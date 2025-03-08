from functools import lru_cache
from pathlib import Path
from secrets import token_urlsafe
from sys import stdout

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from slowapi import Limiter
from slowapi.util import get_remote_address

logger.add(stdout, colorize=True, level="INFO")
limiter = Limiter(key_func=get_remote_address)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )
    # A directory for storing files used in tests
    TEST_STATIC_DIR: Path = Path().parent.parent / "tests" / "static"
    # Data that will be shown in Swagger UI
    APP_INFO: dict = {
        "title": "File metadata extractor API",
        "description": "No description.",  # Markdown
        "summary": "No summary.",
        "version": "0.0.1",
        "terms_of_service": "https://broken_link.unknown",
        "contact": {
            "email": "default@example.com",
            "url": "https://broken_link.unknown",
        },
        "license_info": {
            "name": "Unlicense",
            "identifier": "Unlicense",
            "url": "https://unlicense.org/",
        },
    }
    TAG_METADATA: list[dict] = [
        {
            "name": "metadata",
            "description": "Metadata extracting operations.",
            "external_docs": {
                "description": "No description",
                "url": "https://broken_link.unknown",
            },
        }
    ]
    # Cross-Origin Resource Sharing (CORS)
    ALLOWED_ORIGINS: list[str] = []
    ALLOWED_CREDENTIALS: bool = False
    ALLOWED_METHODS: list[str] = []
    ALLOWED_HEADERS: list[str] = []
    # JWT
    JWT_SECRET: str = token_urlsafe(32)
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URI: str = "sqlite:///sqlite.db"
    FIRST_SUPERUSER_USERNAME: str = "superuser"
    FIRST_SUPERUSER_PASSWORD: str = "secret897"


# Using a function for settings allows it to be used as a dependency
# in endpoints, making it possible to override it in tests
@lru_cache  # Optimize performance by caching
def get_settings():
    return Settings()
