from typing import List, Optional
from fastapi import APIRouter, Depends, Security
from sqlalchemy import text
from sqlalchemy.orm import Session

from core.security import get_current_user
from db.database import get_db
from schemas.auth import User
from schemas.search import SearchResult
from services.vectorSearch import VectorSearchService

vector_search_service = VectorSearchService()
router = APIRouter(tags=['Search'])


def format_tsquery(query: str) -> str:
    """
    Format a user's search query into a valid tsquery string.
    Handles special characters and converts to basic AND operation.
    """
    # Remove any special characters and split into words
    words = [word for word in query.split() if word.isalnum()]
    if not words:
        return "''"  # Return empty query if no valid words
    # Join words with & (AND) operator
    return ' & '.join(f"'{word}'" for word in words)


@router.get("/search/", response_model=List[SearchResult])
async def search_documents_full_content(
        query: str,
        user: User = Security(get_current_user, scopes=["file:read"]),
        db: Session = Depends(get_db)
):
    """
    Search through document content and return full documents with all matches highlighted.
    Features:
    - Returns complete document content with all matches highlighted
    - Uses PostgreSQL's ts_headline with custom configuration
    - Maintains search ranking
    - Preserves document structure
    - Handles multi-word searches
    """
    # Generate tsvector on-the-fly since we haven't added the column yet
    search_query = text("""
        WITH search_results AS (
            SELECT 
                fm.id,
                fm.filename,
                fm.content_type,
                fm.content,
                ts_rank(to_tsvector('english', fm.content), plainto_tsquery('english', :query)) as rank
            FROM file_metadata fm
            WHERE to_tsvector('english', fm.content) @@ plainto_tsquery('english', :query)
                AND (fm.user_id = :user_id OR :is_admin)
        )
        SELECT 
            sr.id,
            sr.filename,
            sr.content_type,
            ts_headline(
                'english',
                sr.content,
                plainto_tsquery('english', :query),
                'StartSel = <mark>, 
                 StopSel = </mark>, 
                 MaxFragments = 0,
                 MinWords = 1,
                 MaxWords = 10000000,
                 ShortWord = 2,
                 HighlightAll = true'
            ) as content_preview,
            sr.rank
        FROM search_results sr
        ORDER BY sr.rank DESC
        LIMIT 10
    """)

    # Execute the search query
    try:
        results = db.execute(
            search_query,
            {
                "query": query,
                "user_id": user.sub,
                "is_admin": "admin" in user.roles
            }
        )

        # Convert the results to a list of SearchResult objects
        search_results = []
        for row in results:
            search_results.append({
                "file_id": row.id,
                "filename": row.filename,
                "content_type": row.content_type,
                "content_preview": row.content_preview,
                "rank": float(row.rank)
            })

        return search_results

    except Exception as e:
        print(f"Search error: {str(e)}")
        return []


@router.get("/contextualsearch/", response_model=List[SearchResult])
async def search_documents_contextual_content(
        query: str,
        user: User = Security(get_current_user, scopes=["file:read"]),
        db: Session = Depends(get_db)
):
    """
    Search through document content and return contextual snippets with matches highlighted.
    """
    return vector_search_service.search_by_vector(db, query)
