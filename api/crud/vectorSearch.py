from typing import Dict

from sqlalchemy import select, and_, or_, not_, text
from sqlalchemy.orm import Session


from models.file import FileEmbedding, FileMetadata

keyword_to_sql = {
    'AND': 'AND',
    'OR': 'OR',
    '&&': 'AND',
    '||': 'OR'
}


def create_vector_entries(db: Session, vectors, file_id: str):
    """Create new vector entries"""
    db_vectors = map(lambda v: FileEmbedding(file_id=file_id, **v), vectors)
    db.add_all(db_vectors)
    db.commit()


def parse(q, depth=0):
    if not q:
        return None, dict()

    for i in range(1, len(q)):
        for key in keyword_to_sql:
            if q[:i].endswith(key):
                keyword = keyword_to_sql[key]
                if keyword == "AND":
                    prev_word = text(f"file_metadata.content ILIKE :filter_{depth}")
                    next_word, next_params = parse(q[i:].strip(), depth=depth + 1)
                    return and_(prev_word, next_word), next_params | {f"filter_{depth}": f"%{q[:i - len(key)].strip()}%"}

                elif keyword == "OR":
                    prev_word = text(f"file_metadata.content ILIKE :filter_{depth}")
                    next_word, next_params = parse(q[i:].strip(), depth=depth + 1)
                    return or_(prev_word, next_word), next_params | {f"filter_{depth}": f"%{q[:i - len(key)].strip()}%"}

    return text(f"file_metadata.content ILIKE :filter_{depth}"), {f"filter_{depth}": f"%{q.strip()}%"}


def search_by_vector(db: Session, query_vector, query_text: str):
    """
    Search for documents using vector similarity and text-based filters.

    Args:
        db: SQLAlchemy database session
        query_vector: Vector to compare against document embeddings
        query_text: Text query containing keywords for filtering

    Returns:
        List of results containing embeddings, metadata, and distance scores
    """

    # Build text-based filter conditions and collect parameters
    query_parsed, params = parse(query_text)
    print(type(query_parsed))

    # Combine all filter conditions
    combined_filters = and_(
        FileEmbedding.embedding.cosine_distance(query_vector) < 0.5,
        query_parsed
    ) if query_parsed is not None else FileEmbedding.embedding.cosine_distance(query_vector) < 0.5

    # Build and execute query
    query = (
        select(FileEmbedding, FileMetadata, FileEmbedding.embedding.cosine_distance(query_vector).label('distance'))
        .join(FileMetadata, FileMetadata.id == FileEmbedding.file_id)
        .filter(combined_filters)
        .order_by(FileEmbedding.embedding.cosine_distance(query_vector))
        .limit(10)
    )

    # Execute query with parameters
    print(query)
    results = db.execute(query, params).all()
    return results
