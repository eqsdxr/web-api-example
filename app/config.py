from sys import stdout
from pathlib import Path
from loguru import logger

test_static_dir = Path().parent.parent / "app" / "tests" / "static"

logger.add(
    stdout, colorize=True, format="{time} {level} {message}", level="INFO"
)
