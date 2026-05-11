import logging
from fastapi import APIRouter, Depends, HTTPException
from src.core.config import get_settings
from src.core.security import require_api_key
from src.models.chat import ChatRequest, ChatResponse
from src.services.chat_orchestrator import ChatOrchestrator
from src.services.openai_service import LLMService
from src.services.qdrant_service import VectorStoreService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse, dependencies=[Depends(require_api_key)])
def chat(request: ChatRequest) -> ChatResponse:
    try:
        settings = get_settings()
        llm = LLMService(settings)
        vector_store = VectorStoreService(settings)
        orchestrator = ChatOrchestrator(settings, llm, vector_store)
        return orchestrator.answer(request)
    except Exception as exc:
        logger.exception("Erro ao processar conversa RAG")
        raise HTTPException(status_code=500, detail=f"Erro ao processar conversa RAG: {exc}") from exc
