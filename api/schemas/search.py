from pydantic import BaseModel

class SearchResult(BaseModel):
    file_id: str
    filename: str
    content_type: str
    content_preview: str
    rank: float
    
    class Config:
        from_attributes = True
