from datetime import datetime
from typing import Dict, Any

from pydantic import BaseModel


class FileInfo(BaseModel):
    """Schema for file information with additional fields"""
    fileId: str
    filename: str
    size: int
    last_modified: str


class FileMetadataResponse(BaseModel):
    """Schema for file metadata response"""
    file_id: str
    filename: str
    content_type: str
    file_metadata: Dict[str, Any]
    content: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class FileUploadResponse(BaseModel):
    """Schema for file upload response"""
    message: str
    file_id: str
    docling_processed: bool


class FileDeleteResponse(BaseModel):
    """Schema for file delete response"""
    message: str
