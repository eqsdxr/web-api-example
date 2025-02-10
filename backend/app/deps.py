from typing import Generator

from sqlalchemy import create_engine, Connection

from app.config import main_config

engine = create_engine(main_config["database_url"], echo=True)


def get_db() -> Generator[Connection, None, None]:
    with engine.connect() as conn:
        yield conn
