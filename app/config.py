from functools import lru_cache
from pathlib import Path
from secrets import token_urlsafe
from sys import stdout

from loguru import logger
from pydantic_settings import BaseSettings

logger.add(stdout, colorize=True, level="INFO")


class Settings(BaseSettings):
    # A directory for storing files used in tests
    test_static_dir: Path = Path().parent.parent / "tests" / "static"
    # Data that will be shown in Swagger UI
    app_info: dict = {
        "title": "File metadata extractor API",
        "description": "No description.",  # Markdown is possible to be used here
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
    # JWT
    jwt_secret: str = token_urlsafe(32)
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60

    database_uri: str = "sqlite:///:memory:"
    first_superuser_username: str = "superuser"
    first_superuser_password: str = "secret897"


# It makes sense to use a function for settings because it can be used
# as a dependency in endpoints which then can be overriden for tests
@lru_cache  # Optimize performance by caching
def get_settings():
    return Settings()
