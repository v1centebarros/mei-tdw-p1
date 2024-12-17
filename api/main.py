import uuid
from typing import List, Optional
from datetime import timedelta

from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, Security
from fastapi.security import OAuth2AuthorizationCodeBearer, OAuth2PasswordBearer, HTTPBearer, \
    HTTPAuthorizationCredentials
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from minio import Minio
from minio.error import S3Error

from keycloak import KeycloakOpenID, KeycloakAdmin
from keycloak.exceptions import KeycloakGetError
from keycloak.exceptions import KeycloakError

# Keycloak settings
KEYCLOAK_URL = "http://localhost:8080"
KEYCLOAK_REALM = "TDW"
KEYCLOAK_CLIENT_ID = "tdw-client"
KEYCLOAK_CLIENT_SECRET = "WnM69tiQwcscM9Ix0f5TXppHOuS917lm"
KEYCLOAK_ALGORITHM = "RS256"

# Initialize Keycloak clients
# OAuth client for token validation and user authentication
keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET
)

app = FastAPI(title="FastAPI MinIO CRUD")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth2 scheme for Swagger UI
oauth2_scheme = HTTPBearer()

# Initialize MinIO client
minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

# Default bucket name
BUCKET_NAME = "fastapi-bucket"

# Ensure bucket exists
try:
    if not minio_client.bucket_exists(BUCKET_NAME):
        minio_client.make_bucket(BUCKET_NAME)
except S3Error as e:
    print(f"Error creating bucket: {e}")


class FileInfo(BaseModel):
    fileId: str
    filename: str
    size: int
    last_modified: str


class User(BaseModel):
    username: str
    roles: List[str]
    sub: str


class UserRegistration(BaseModel):
    username: str
    email: str
    password: str
    firstName: str
    lastName: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    refresh_expires_in: int
    token_type: str


# Initialize Keycloak admin client
keycloak_admin = KeycloakAdmin(
    server_url=KEYCLOAK_URL,
    realm_name=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT_ID,
    client_secret_key=KEYCLOAK_CLIENT_SECRET,
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
        user: User = Security(get_current_user, scopes=["file:write"])
):
    """
    Upload a file to MinIO storage
    """
    try:
        file_id = uuid.uuid4().hex

        # Upload to MinIO with user metadata
        minio_client.put_object(
            BUCKET_NAME,
            file_id,
            length=file.size,
            data=file.file,
            metadata={
                "filename": file.filename,
                "user_id": user.sub,
                "username": user.username
            },
            part_size=10 * 1024 * 1024  # 10MB parts
        )

        return {"message": f"Successfully uploaded {file.filename}", "file_id": file_id}
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()


@app.get("/files/", response_model=List[FileInfo])
async def list_files(
        user: User = Security(get_current_user, scopes=["file:read"])
):
    """
    List all files in the storage
    """
    try:
        objects = minio_client.list_objects(BUCKET_NAME)
        files = []
        for obj in objects:
            # Get object metadata
            stat = minio_client.stat_object(BUCKET_NAME, obj.object_name)
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
        stat = minio_client.stat_object(BUCKET_NAME, file_id)

        # Check if user has access to the file
        if user.sub != stat.metadata.get("x-amz-meta-user_id") and "admin" not in user.roles:
            raise HTTPException(status_code=403, detail="Access denied")

        # Get object data
        data = minio_client.get_object(BUCKET_NAME, file_id)
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
        user: User = Security(get_current_user, scopes=["file:write"])
):
    """
    Delete a file from storage
    """
    try:
        # Get object metadata
        stat = minio_client.stat_object(BUCKET_NAME, file_id)

        # Check if user has access to the file
        if user.sub != stat.metadata.get("x-amz-meta-user_id") and "admin" not in user.roles:
            raise HTTPException(status_code=403, detail="Access denied")

        minio_client.remove_object(BUCKET_NAME, file_id)
        return {"message": f"Successfully deleted {stat.metadata.get('x-amz-meta-filename', file_id)}"}
    except S3Error as e:
        raise HTTPException(status_code=404, detail="File not found")
