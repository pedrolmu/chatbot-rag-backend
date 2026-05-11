from openai import OpenAI
from src.core.config import Settings
from src.models.chat import ChatMessage


class LLMService:
    """Centraliza o acesso ao modelo de linguagem e aos embeddings.

    A ideia é deixar a troca de provedor concentrada neste serviço, sem espalhar
    chamadas de API pelas rotas.
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY não foi configurada no arquivo .env.")
        self.client = OpenAI(api_key=settings.openai_api_key)

    def create_embedding(self, text: str) -> list[float]:
        response = self.client.embeddings.create(
            model=self.settings.openai_embedding_model,
            input=text,
        )
        return response.data[0].embedding

    def create_chat_response(
        self,
        system_message: str,
        user_message: str,
        history: list[ChatMessage] | None = None,
    ) -> str:
        messages = [{"role": "system", "content": system_message}]

        for item in history or []:
            if item.role in {"user", "assistant", "system"}:
                messages.append({"role": item.role, "content": item.content})

        messages.append({"role": "user", "content": user_message})

        response = self.client.chat.completions.create(
            model=self.settings.openai_chat_model,
            messages=messages,
            temperature=0.2,
        )
        return response.choices[0].message.content or "Não consegui gerar uma resposta."
