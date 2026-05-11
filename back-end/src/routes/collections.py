import logging
from fastapi import APIRouter, Depends, HTTPException
from src.core.config import get_settings
from src.core.security import require_api_key
from src.models.collection import CollectionResponse, DocumentIngestRequest, IngestResponse
from src.services.ingestion_service import IngestionService
from src.services.openai_service import LLMService
from src.services.qdrant_service import VectorStoreService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/collections", tags=["collections"])


@router.get("/default", response_model=CollectionResponse, dependencies=[Depends(require_api_key)])
def get_default_collection() -> CollectionResponse:
    try:
        settings = get_settings()
        vector_store = VectorStoreService(settings)
        data = vector_store.describe_collection()
        return CollectionResponse(**data)
    except Exception as exc:
        logger.exception("Erro ao consultar coleção vetorial")
        raise HTTPException(status_code=500, detail=f"Erro ao consultar coleção vetorial: {exc}") from exc


@router.post("/ingest", response_model=IngestResponse, dependencies=[Depends(require_api_key)])
def ingest_document(request: DocumentIngestRequest) -> IngestResponse:
    try:
        settings = get_settings()
        llm = LLMService(settings)
        vector_store = VectorStoreService(settings)
        service = IngestionService(settings, llm, vector_store)
        count = service.ingest_text(source=request.source, text=request.text)
        return IngestResponse(
            collection=settings.qdrant_collection,
            chunks_indexed=count,
            message="Documento indexado com sucesso no banco vetorial.",
        )
    except Exception as exc:
        logger.exception("Erro ao indexar documento")
        raise HTTPException(status_code=500, detail=f"Erro ao indexar documento: {exc}") from exc
