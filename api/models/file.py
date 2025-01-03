from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, Integer
from pgvector.sqlalchemy import Vector

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


class FileEmbedding(Base):
    __tablename__ = "file_embeddings"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    file_id = Column(String, ForeignKey("file_metadata.id"))
    embedding = Column(Vector(384))
    start_position = Column(Integer)
    end_position = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
