from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., examples=["user", "assistant", "system"])
    content: str = Field(..., min_length=1)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    history: list[ChatMessage] = Field(default_factory=list)
    collection: str | None = None


class SourceDocument(BaseModel):
    source: str
    score: float
    chunk_index: int | None = None
    content: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[SourceDocument] = Field(default_factory=list)
