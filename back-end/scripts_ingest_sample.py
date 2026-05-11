from pathlib import Path
from dotenv import load_dotenv
from src.core.config import get_settings
from src.services.ingestion_service import IngestionService
from src.services.openai_service import LLMService
from src.services.qdrant_service import VectorStoreService


def main() -> None:
    load_dotenv()
    settings = get_settings()
    text = Path("data/docs/exemplo_motor_eletrico.txt").read_text(encoding="utf-8")

    service = IngestionService(
        settings=settings,
        llm=LLMService(settings),
        vector_store=VectorStoreService(settings),
    )
    count = service.ingest_text("exemplo_motor_eletrico.txt", text)
    print(f"{count} chunks indexados em {settings.qdrant_collection}")


if __name__ == "__main__":
    main()
