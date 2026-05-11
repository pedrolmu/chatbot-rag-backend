from pydantic import BaseModel, Field


class DocumentIngestRequest(BaseModel):
    source: str = Field(..., min_length=1)
    text: str = Field(..., min_length=10)


class IngestResponse(BaseModel):
    collection: str
    chunks_indexed: int
    message: str


class CollectionResponse(BaseModel):
    name: str
    vectors_count: int | None = None
    status: str | None = None
