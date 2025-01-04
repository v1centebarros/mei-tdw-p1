from sqlalchemy import select
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import Session


from models.file import FileEmbedding, FileMetadata


def create_vector_entries(db: Session, vectors, file_id: str):
    """Create new vector entries"""
    db_vectors = map(lambda v: FileEmbedding(file_id=file_id, **v), vectors)
    db.add_all(db_vectors)
    db.commit()


def search_by_vector(db: Session, query_vector):
    query = (
        select(FileEmbedding, FileMetadata, FileEmbedding.embedding.cosine_distance(query_vector).label('distance'))
        .join(FileMetadata, FileMetadata.id == FileEmbedding.file_id)
        .filter(FileEmbedding.embedding.cosine_distance(query_vector) < 0.5)
        .order_by(FileEmbedding.embedding.cosine_distance(query_vector))
        .limit(10)
    )

    results = db.execute(query).all()
    return results
