from datetime import datetime
from sqlalchemy import Column, String, JSON, DateTime

from db.database import Base


class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id = Column(String, primary_key=True)
    filename = Column(String)
    content_type = Column(String)
    file_metadata = Column(JSON)
    content = Column(String)
    user_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)