from src.core.config import Settings
from src.models.chat import ChatRequest, ChatResponse, SourceDocument
from src.services.openai_service import LLMService
from src.services.qdrant_service import VectorStoreService


class ChatOrchestrator:
    def __init__(self, settings: Settings, llm: LLMService, vector_store: VectorStoreService):
        self.settings = settings
        self.llm = llm
        self.vector_store = vector_store

    def answer(self, request: ChatRequest) -> ChatResponse:
        query_embedding = self.llm.create_embedding(request.message)
        results = self.vector_store.search(
            query_vector=query_embedding,
            collection_name=request.collection,
            top_k=self.settings.top_k,
        )

        context_blocks = []
        sources: list[SourceDocument] = []
        for item in results:
            payload = item.payload or {}
            text = payload.get("text", "")
            context_blocks.append(f"Fonte: {payload.get('source')} | Trecho: {text}")
            sources.append(
                SourceDocument(
                    source=payload.get("source", "documento"),
                    score=float(item.score),
                    chunk_index=payload.get("chunk_index"),
                    content=text,
                )
            )

        system_message = (
            "Você é um assistente RAG técnico, claro e objetivo. "
            "Responda em português do Brasil, usando apenas o contexto recuperado quando a pergunta depender dos documentos. "
            "Se o contexto não tiver a resposta, diga isso com honestidade e sugira o próximo passo.\n\n"
            "CONTEXTO RECUPERADO:\n" + "\n---\n".join(context_blocks)
        )
        answer = self.llm.create_chat_response(system_message, request.message, request.history)
        return ChatResponse(answer=answer, sources=sources)
