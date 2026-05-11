from src.core.config import Settings
from src.services.openai_service import LLMService
from src.services.qdrant_service import VectorStoreService
from src.utils.chunking import chunk_text


class IngestionService:
    def __init__(self, settings: Settings, llm: LLMService, vector_store: VectorStoreService):
        self.settings = settings
        self.llm = llm
        self.vector_store = vector_store

    def ingest_text(self, source: str, text: str, collection_name: str | None = None) -> int:
        chunks = chunk_text(text, source, self.settings.max_chunk_size, self.settings.chunk_overlap)
        vectors = [self.llm.create_embedding(chunk.text) for chunk in chunks]
        payloads = [{**chunk.metadata, "text": chunk.text} for chunk in chunks]
        return self.vector_store.upsert_documents(vectors, payloads, collection_name)
