from fastapi import APIRouter, Depends, Security
from db.database import get_db
from core.security import get_current_user
from sqlalchemy.orm import Session
from schemas.auth import User

from services.chat import RAGPipeline
from sse_starlette.sse import EventSourceResponse

router = APIRouter(tags=['Chat'])
rag_pipeline = RAGPipeline("services/model.gguf")

@router.get("/chat/", status_code=200)
async def chat(
        question: str,
        user: User = Security(get_current_user, scopes=["file:write"]),
        db: Session = Depends(get_db),
):
    response_stream = rag_pipeline.query_documents(db, question, user.sub)

    return EventSourceResponse(response_stream, media_type="text/event-stream")

