from typing import Generator

from sqlmodel import Session, create_engine

from app.config import main_config

engine = create_engine(main_config.database_url, echo=True)


def get_db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
