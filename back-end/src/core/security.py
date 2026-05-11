from fastapi import Header, HTTPException, status
from src.core.config import get_settings


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    settings = get_settings()
    if settings.environment == "development" and settings.api_key == "dev-key":
        return
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API key inválida ou ausente.")
