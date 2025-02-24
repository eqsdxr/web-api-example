from sys import stdout
from pathlib import Path
from loguru import logger

test_static_dir = Path().parent.parent / "app" / "tests" / "static"

logger.add(
    stdout, colorize=True, format="{time} {level} {message}", level="INFO"
)

app_info = {
    "title": "File metadata extractor API",
    "description": "__No description.__",
    "summary": "No summary.",
    "version": "0.0.1",
    "terms_of_service": "Nothing special.",
    "contact": {"email": "default@example.com", "url": "broken-link"},
    "license_info": {
        "name": "Unlicense",
        "identifier": "Unlicense",
        "url": "https://unlicense.org/",
    },
}

tags_metadata = [
    {
        "name": "metadata",
        "description": "Metadata extracting operations.",
        "external_docs": {
            "description": "No description",
            "url": "broken-link",
        },
    }
]
