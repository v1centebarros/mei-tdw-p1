import io
import os
import uuid
from typing import List

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.security import HTTPAuthorizationCredentials
from keycloak import KeycloakAdmin
from keycloak.exceptions import KeycloakError
from keycloak.exceptions import KeycloakGetError
from minio.error import S3Error
from sqlalchemy.orm import Session

from core.config import get_settings
from core.minio import init_minio, minio_client
from core.security import oauth2_scheme, keycloak_openid
from crud import file as file_crud
from db.database import engine, SessionLocal
from models.file import Base
from schemas.auth import UserRegistration, TokenResponse, UserLogin, User
from schemas.file import FileInfo

# Load environment variables
load_dotenv()

settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)


# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TIKA server URL from environment
TIKA_URL = os.getenv('TIKA_URL')


# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


init_minio()

# Initialize Keycloak admin client
keycloak_admin = KeycloakAdmin(
    server_url=settings.KEYCLOAK_URL,
    realm_name=settings.KEYCLOAK_REALM,
    client_id=settings.KEYCLOAK_CLIENT_ID,
    client_secret_key=settings.KEYCLOAK_CLIENT_SECRET,
    verify=True
)


@app.post("/auth/register", response_model=dict)
async def register_user(user_data: UserRegistration):
    """
    Register a new user in Keycloak
    """
    try:
        # Create user in Keycloak
        new_user = keycloak_admin.create_user({
            "username": user_data.username,
            "email": user_data.email,
            "enabled": True,
            "firstName": user_data.firstName,
            "lastName": user_data.lastName,
            "credentials": [{
                "type": "password",
                "value": user_data.password,
                "temporary": False
            }]
        })

        # Get the user id
        user_id = keycloak_admin.get_user_id(user_data.username)

        # Get role representations
        roles = keycloak_admin.get_realm_roles()
        file_read_role = next((role for role in roles if role['name'] == 'file:read'), None)
        file_write_role = next((role for role in roles if role['name'] == 'file:write'), None)

        # Format roles for assignment
        roles_to_assign = []
        if file_read_role:
            roles_to_assign.append(file_read_role)
        if file_write_role:
            roles_to_assign.append(file_write_role)

        # Assign roles if they exist
        if roles_to_assign:
            keycloak_admin.assign_realm_roles(
                user_id=user_id,
                roles=roles_to_assign
            )

        return {"message": "User registered successfully"}
    except KeycloakGetError as e:
        if "username already exists" in str(e):
            raise HTTPException(
                status_code=400,
                detail="Username already exists"
            )
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/login", response_model=TokenResponse)
async def login_user(user_credentials: UserLogin):
    """
    Login user and return access token
    """
    try:
        # Get token from Keycloak
        token = keycloak_openid.token(
            username=user_credentials.username,
            password=user_credentials.password
        )

        return TokenResponse(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            expires_in=token["expires_in"],
            refresh_expires_in=token["refresh_expires_in"],
            token_type=token["token_type"]
        )
    except KeycloakError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token
    """
    try:
        token = keycloak_openid.refresh_token(refresh_token)

        return TokenResponse(
            access_token=token["access_token"],
            refresh_token=token["refresh_token"],
            expires_in=token["expires_in"],
            refresh_expires_in=token["refresh_expires_in"],
            token_type=token["token_type"]
        )
    except KeycloakError as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/auth/logout")
async def logout(refresh_token: str):
    """
    Logout user and invalidate refresh token
    """
    try:
        keycloak_openid.logout(refresh_token)
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_current_user(credentials: HTTPAuthorizationCredentials = Security(oauth2_scheme)) -> User:
    try:
        # Decode token and verify signature
        token = credentials.credentials  # This is the bearer token
        token_info = keycloak_openid.decode_token(
            token,
        )

        # Extract user information
        return User(
            username=token_info.get("preferred_username", ""),
            roles=token_info.get("realm_access", {}).get("roles", []),
            sub=token_info.get("sub", "")
        )
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(required_roles: List[str]):
    async def role_checker(user: User = Security(get_current_user)):
        for role in required_roles:
            if role not in user.roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Role {role} is required"
                )
        return user

    return role_checker


@app.post("/upload/", status_code=201)
async def upload_file(
        file: UploadFile = File(...),
        user: User = Security(get_current_user, scopes=["file:write"]),
        db: Session = Depends(get_db)
):
    """
    Upload a file to MinIO storage and process with TIKA
    """
    try:
        file_id = uuid.uuid4().hex
        file_content = await file.read()  # Read file content

        # Upload to MinIO with user metadata
        minio_client.put_object(
            settings.MINIO_BUCKET_NAME,
            file_id,
            length=len(file_content),
            data=io.BytesIO(file_content),
            metadata={
                "filename": file.filename,
                "user_id": user.sub,
                "username": user.username
            },
            part_size=10 * 1024 * 1024  # 10MB parts
        )

        # Send to TIKA for content extraction
        try:
            print(file.content_type)
            # Extract content
            tika_content_response = requests.put(
                f"{TIKA_URL}/tika",
                data=file_content,
                headers={
                    'Accept': 'text/plain; charset=UTF-8',
                    'Content-Type': f'{file.content_type}'
                }
            )
            tika_content = tika_content_response.text

            # Extract metadata
            tika_metadata_response = requests.put(
                f"{TIKA_URL}/meta",
                data=file_content,
                headers={'Accept': 'application/json'}
            )
            tika_metadata = tika_metadata_response.json()

            # Store in PostgreSQL
            file_crud.create_file_metadata(
                db=db,
                file_id=file_id,
                filename=file.filename,
                content_type=file.content_type,
                tika_metadata=tika_metadata,
                content=tika_content,
                user_id=user.sub
            )

        except requests.RequestException as e:
            print(f"TIKA processing error: {e}")
            # Continue even if TIKA fails
            pass

        return {
            "message": f"Successfully uploaded {file.filename}",
            "file_id": file_id,
            "tika_processed": True
        }

    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()


# Add new endpoint to get file metadata
@app.get("/files/{file_id}/metadata")
async def get_file_metadata(
        file_id: str,
        user: User = Security(get_current_user, scopes=["file:read"]),
        db: Session = Depends(get_db)
):
    """
    Get file metadata including TIKA extraction results
    """
    # Query the database for file metadata
    file_metadata = file_crud.get_file_metadata(db, file_id)

    if not file_metadata:
        raise HTTPException(status_code=404, detail="File metadata not found")

    # Check if user has access to the file
    if not file_crud.user_owns_file(db, file_id, user.sub) and "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Access denied")

    return {
        "file_id": file_metadata.id,
        "filename": file_metadata.filename,
        "content_type": file_metadata.content_type,
        "metadata": file_metadata.tika_metadata,
        "content": file_metadata.content,
        "created_at": file_metadata.created_at,
        "updated_at": file_metadata.updated_at
    }


@app.get("/files/", response_model=List[FileInfo])
async def list_files(
        user: User = Security(get_current_user, scopes=["file:read"])
):
    """
    List all files in the storage
    """
    try:
        objects = minio_client.list_objects(settings.MINIO_BUCKET_NAME)
        files = []
        for obj in objects:
            # Get object metadata
            stat = minio_client.stat_object(settings.MINIO_BUCKET_NAME, obj.object_name)
            # Check if user has access to the file
            if user.sub == stat.metadata.get("x-amz-meta-user_id") or "admin" in user.roles:
                files.append(
                    FileInfo(
                        fileId=obj.object_name,
                        filename=stat.metadata.get("x-amz-meta-filename", obj.object_name),
                        size=obj.size,
                        last_modified=obj.last_modified.strftime("%Y-%m-%d %H:%M:%S")
                    )
                )
        return files
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/files/{file_id}")
async def download_file(
        file_id: str,
        user: User = Security(get_current_user, scopes=["file:read"])
):
    """
    Download a file from storage
    """
    try:
        # Get object metadata
        stat = minio_client.stat_object(settings.MINIO_BUCKET_NAME, file_id)

        # Check if user has access to the file
        if user.sub != stat.metadata.get("x-amz-meta-user_id") and "admin" not in user.roles:
            raise HTTPException(status_code=403, detail="Access denied")

        # Get object data
        data = minio_client.get_object(settings.MINIO_BUCKET_NAME, file_id)
        filename = stat.metadata.get("x-amz-meta-filename", file_id)

        # Create generator for streaming response
        def iterfile():
            try:
                yield from data
            finally:
                data.close()
                data.release_conn()

        # Return streaming response
        return StreamingResponse(
            iterfile(),
            media_type="application/octet-stream",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except S3Error as e:
        raise HTTPException(status_code=404, detail="File not found")


@app.delete("/files/{file_id}")
async def delete_file(
        file_id: str,
        user: User = Security(get_current_user, scopes=["file:write"]),
        db: Session = Depends(get_db)
):
    """
    Delete a file from storage and its associated metadata
    """
    try:
        # Get object metadata from MinIO
        stat = minio_client.stat_object(settings.MINIO_BUCKET_NAME, file_id)

        # Check if user has access to the file
        if not file_crud.user_owns_file(db, file_id, user.sub)  and "admin" not in user.roles:
            raise HTTPException(status_code=403, detail="Access denied")

        # Delete from MinIO
        minio_client.remove_object(settings.MINIO_BUCKET_NAME, file_id)

        # Delete metadata from PostgreSQL
        if file_crud.delete_file_metadata(db, file_id):
            return {
                "message": f"Successfully deleted {stat.metadata.get('x-amz-meta-filename', file_id)} and its metadata"
            }
        else:
            raise HTTPException(status_code=404, detail="File metadata not found")
    except S3Error as e:
        raise HTTPException(status_code=404, detail="File not found")
