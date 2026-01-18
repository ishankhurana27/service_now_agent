from pydantic import BaseModel, Field
from typing import Optional


class IngestResponse(BaseModel):
    pdfs_ingested: int
    chunks_created: int


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    session_id: Optional[str] = None


class QueryResponse(BaseModel):
    answer: str
    article_id: str
    intent: str
    session_id: str
