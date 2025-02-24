from sys import stdout
from pathlib import Path
from functools import lru_cache

from loguru import logger
from pydantic_settings import BaseSettings

logger.add(stdout, colorize=True, level="INFO")


class Settings(BaseSettings):
    # A directory for storing files used in tests
    test_static_dir: Path = Path().parent.parent / "app" / "tests" / "static"
    app_info: dict = {
        "title": "File metadata extractor API",
        "description": "__No description.__",
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
    tags_metadata: list[dict] = [
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
    allowed_origins: list[str] = []
    allowed_credentials: bool = False
    allowed_methods: list[str] = []
    allowed_headers: list[str] = []


@lru_cache  # Optimize performance by caching
def get_settings():
    return Settings()
