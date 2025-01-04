# app/crud/file.py
from typing import List, Optional, Type
from sqlalchemy.orm import Session
from datetime import datetime

from models.file import FileMetadata


def create_file_metadata(
        db: Session,
        file_id: str,
        filename: str,
        content_type: str,
        file_metadata: dict,
        content: str,
        categories: list[str],
        user_id: str
) -> FileMetadata:
    """Create new file metadata entry"""
    db_file = FileMetadata(
        id=file_id,
        filename=filename,
        content_type=content_type,
        file_metadata=file_metadata,
        categories=categories,
        content=content,
        user_id=user_id
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def get_file_metadata(
        db: Session,
        file_id: str
) -> Optional[FileMetadata]:
    """Get file metadata by ID"""
    return db.query(FileMetadata).filter(FileMetadata.id == file_id).first()


def get_user_files(
        db: Session,
        user_id: str
) -> List[FileMetadata]:
    """Get all files for a specific user"""
    return db.query(FileMetadata).filter(FileMetadata.user_id == user_id).all()


def get_all_files(
        db: Session
) -> list[Type[FileMetadata]]:
    """Get all files (admin only)"""
    return db.query(FileMetadata).all()


def update_file_metadata(
        db: Session,
        file_id: str,
        file_metadata: dict,
        content: str,
        categories: list[str]
) -> Optional[FileMetadata]:
    """Update file metadata"""
    db_file = get_file_metadata(db, file_id)
    if db_file:
        db_file.file_metadata = file_metadata
        db_file.content = content
        db_file.categories = categories
        db_file.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_file)
    return db_file


def delete_file_metadata(
        db: Session,
        file_id: str
) -> bool:
    """Delete file metadata"""
    db_file = get_file_metadata(db, file_id)
    if db_file:
        db.delete(db_file)
        db.commit()
        return True
    return False


def user_owns_file(
        db: Session,
        file_id: str,
        user_id: str
) -> bool:
    """Check if user owns the file"""
    db_file = get_file_metadata(db, file_id)
    return db_file is not None and db_file.user_id == user_id
