from typing import BinaryIO, Dict, Optional
from minio.error import S3Error
from fastapi import HTTPException

from core.config import get_settings
from core.minio import minio_client

settings = get_settings()


class MinioService:
    def __init__(self):
        self.client = minio_client
        self.bucket_name = settings.MINIO_BUCKET_NAME

    async def upload_file(
            self,
            file_id: str,
            file_data: BinaryIO,
            file_size: int,
            metadata: Dict[str, str]
    ) -> bool:
        """Upload a file to MinIO"""
        try:
            self.client.put_object(
                self.bucket_name,
                file_id,
                data=file_data,
                length=file_size,
                metadata=metadata,
                part_size=10 * 1024 * 1024  # 10MB parts
            )
            return True
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")

    def download_file(self, file_id: str) -> tuple[BinaryIO, Dict[str, str]]:
        """Download a file from MinIO"""
        try:
            data = self.client.get_object(self.bucket_name, file_id)
            stat = self.client.stat_object(self.bucket_name, file_id)
            return data, stat.metadata
        except S3Error:
            raise HTTPException(status_code=404, detail="File not found")

    def delete_file(self, file_id: str) -> bool:
        """Delete a file from MinIO"""
        try:
            self.client.remove_object(self.bucket_name, file_id)
            return True
        except S3Error:
            raise HTTPException(status_code=404, detail="File not found")

    def get_file_metadata(self, file_id: str) -> Dict[str, str]:
        """Get file metadata from MinIO"""
        try:
            stat = self.client.stat_object(self.bucket_name, file_id)
            return stat.metadata
        except S3Error:
            raise HTTPException(status_code=404, detail="File not found")

    def list_files(self) -> list[Dict[str, str]]:
        """List all files in MinIO bucket"""
        try:
            objects = self.client.list_objects(self.bucket_name)
            return objects
        except S3Error as e:
            raise HTTPException(status_code=500, detail=f"MinIO error: {str(e)}")