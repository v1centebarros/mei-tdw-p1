import io
import uuid
from typing import List

import requests
from fastapi import APIRouter
from fastapi import HTTPException, UploadFile, File, Depends, Security
from fastapi.responses import StreamingResponse
from minio.error import S3Error
from sqlalchemy.orm import Session

from core.security import get_current_user
from crud import file as file_crud
from crud import vectorSearch as vector_search_crud
from db.database import get_db
from schemas.auth import User
from schemas.file import FileInfo
from services.minio import MinioService
from services.docling import DocumentService
from services.vectorSearch import VectorSearchService

minio_service = MinioService()
document_service = DocumentService()
vector_search_service = VectorSearchService()

router = APIRouter(tags=['File Management'])


@router.post("/upload/", status_code=201)
async def upload_file(
        file: UploadFile = File(...),
        user: User = Security(get_current_user, scopes=["file:write"]),
        db: Session = Depends(get_db)
):
    """
    Upload a file to MinIO storage and process with Docling
    """
    try:
        file_id = uuid.uuid4().hex
        file_content = await file.read()  # Read file content

        # Upload to MinIO with user metadata
        metadata = {
            "filename": file.filename,
            "user_id": user.sub,
            "username": user.username
        }
        minio_entry = await minio_service.upload_file(
            file_id=file_id,
            file_data=io.BytesIO(file_content),
            file_size=len(file_content),
            metadata=metadata
        )

        # Send to Docling for content extraction
        try:
            markdown_content, file_metadata = await document_service.process_file(
                source=minio_entry
            )

            # Store metadata in database
            file_crud.create_file_metadata(
                db=db,
                file_id=file_id,
                filename=file.filename,
                content_type=file.content_type,
                file_metadata=file_metadata,
                content=markdown_content,
                user_id=user.sub
            )


        except requests.RequestException as e:
            print(f"Docling processing error: {e}")
            return

        # embbed the text
        try:
            vectors = vector_search_service.index(markdown_content)
            vector_search_crud.create_vector_entries(db, vectors, file_id)

        except Exception as e:
            print(f"Embedding error: {e}")
            return

        return {
            "message": f"Successfully uploaded {file.filename}",
            "file_id": file_id,
            "docling_processed": True
        }

    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        file.file.close()


@router.post("/upload/bulk/", status_code=201)
async def upload_multiple_files(
        files: list[UploadFile] = File(...),
        user: User = Security(get_current_user, scopes=["file:write"]),
        db: Session = Depends(get_db)
):
    """
    Upload multiple files to MinIO storage and process with Docling

    Returns a list of upload results for each file, including success status and any errors
    """
    results = []

    for file in files:
        try:
            file_id = uuid.uuid4().hex
            file_content = await file.read()

            # Upload to MinIO with user metadata
            metadata = {
                "filename": file.filename,
                "user_id": user.sub,
                "username": user.username
            }

            minio_entry = await minio_service.upload_file(
                file_id=file_id,
                file_data=io.BytesIO(file_content),
                file_size=len(file_content),
                metadata=metadata
            )

            docling_processed = False
            # Send to Docling for content extraction
            try:
                markdown_content, file_metadata = await document_service.process_file(
                    source=minio_entry
                )

                # Store metadata in database
                file_crud.create_file_metadata(
                    db=db,
                    file_id=file_id,
                    filename=file.filename,
                    content_type=file.content_type,
                    file_metadata=file_metadata,
                    content=markdown_content,
                    user_id=user.sub
                )
                docling_processed = True

            except requests.RequestException as e:
                print(f"Docling processing error for {file.filename}: {e}")
                # Continue with next file even if TIKA fails

            results.append({
                "filename": file.filename,
                "file_id": file_id,
                "success": True,
                "docling_processed": docling_processed
            })

        except S3Error as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            })
        finally:
            file.file.close()

    # Calculate summary statistics
    total_files = len(files)
    successful_uploads = len([r for r in results if r["success"]])
    failed_uploads = total_files - successful_uploads

    return {
        "message": f"Processed {total_files} files",
        "summary": {
            "total_files": total_files,
            "successful_uploads": successful_uploads,
            "failed_uploads": failed_uploads
        },
        "results": results
    }


# Add new endpoint to get file metadata
@router.get("/files/{file_id}/metadata")
async def get_file_metadata(
        file_id: str,
        user: User = Security(get_current_user, scopes=["file:read"]),
        db: Session = Depends(get_db)
):
    """
    Get file metadata including Docling extraction results
    """
    # Query the database for file metadata
    file_metadata = file_crud.get_file_metadata(db, file_id)

    if not file_metadata:
        raise HTTPException(status_code=404, detail="File metadata not found")

    # Check if user has access to the file
    if not file_crud.user_owns_file(db, file_id, user.sub) and "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Access denied")

    return file_metadata


@router.get("/files/", response_model=List[FileInfo])
async def list_files(
        user: User = Security(get_current_user, scopes=["file:read"])
):
    """
    List all files in the storage
    """
    try:
        objects = minio_service.list_files()
        files = []
        for obj in objects:
            # Get object metadata
            metadata = minio_service.get_file_metadata(obj.object_name)
            # Check if user has access to the file
            if user.sub == metadata.get("x-amz-meta-user_id") or "admin" in user.roles:
                files.append(
                    FileInfo(
                        fileId=obj.object_name,
                        filename=metadata.get("x-amz-meta-filename", obj.object_name),
                        size=obj.size,
                        last_modified=obj.last_modified.strftime("%Y-%m-%d %H:%M:%S")
                    )
                )
        return files
    except S3Error as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/files/{file_id}")
async def download_file(
        file_id: str,
        user: User = Security(get_current_user, scopes=["file:read"])
):
    """
    Download a file from storage
    """
    # Get object metadata
    metadata = minio_service.get_file_metadata(file_id)

    # Check if user has access to the file
    if user.sub != metadata.get("x-amz-meta-user_id") and "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Access denied")

    data, metadata = minio_service.download_file(file_id)
    filename = metadata.get("x-amz-meta-filename", file_id)

    return StreamingResponse(
        data,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


@router.delete("/files/{file_id}")
async def delete_file(
        file_id: str,
        user: User = Security(get_current_user, scopes=["file:write"]),
        db: Session = Depends(get_db)
):
    """
    Delete a file from storage and its associated metadata
    """
    metadata = minio_service.get_file_metadata(file_id)

    # Check if user has access to the file
    if not file_crud.user_owns_file(db, file_id, user.sub) and "admin" not in user.roles:
        raise HTTPException(status_code=403, detail="Access denied")

    # Delete from MinIO
    minio_service.delete_file(file_id)

    # Delete metadata from PostgreSQL
    if file_crud.delete_file_metadata(db, file_id):
        return {
            "message": f"Successfully deleted {metadata.get('x-amz-meta-filename', file_id)} and its metadata"
        }
    else:
        raise HTTPException(status_code=404, detail="File metadata not found")
