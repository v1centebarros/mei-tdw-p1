from sqlalchemy.orm import Session

from models.file import FileEmbedding


def create_vector_entries(db: Session, vectors, file_id: str):
    """Create new vector entries"""
    db_vectors = map(lambda v: FileEmbedding(file_id=file_id, **v), vectors)
    db.add_all(db_vectors)
    db.commit()

