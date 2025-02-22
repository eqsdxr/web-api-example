from typing import Generator

from sqlmodel import Session, create_engine, SQLModel

from app.config import main_config

# Should I include it in order to be registrated by SQLModel?
from app import models
from app.sec import get_password_hash

engine = create_engine(main_config.database_url)


def get_db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def init_db(session, create_superuser=False):
    SQLModel.metadata.create_all(engine)
    if create_superuser:
        with Session(engine) as session:
            test_user = models.UsersTable(
                username=main_config.first_user_username,
                password_hash=get_password_hash(
                    main_config.first_user_password
                ),
                is_superuser=True,
            )
            session.add(test_user)
            session.commit()
