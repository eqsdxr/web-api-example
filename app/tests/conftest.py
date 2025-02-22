from collections.abc import Generator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlmodel import Session, create_engine, SQLModel, delete

from app.main import app
from app.tests.utils import get_first_user_token_headers
from app.db import get_db_session
from app import models
from app.config import main_config
from app.sec import get_password_hash

test_db = "postgresql+psycopg://postgres:root@localhost/postgres"

test_engine = create_engine(test_db)


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)


def create_first_user(session):
    test_user = models.UsersTable(
        username=main_config.first_user_username,
        password_hash=get_password_hash(main_config.first_user_password),
        is_active=True,
    )
    session.add(test_user)
    session.commit()


def override_get_db_session() -> Generator[Session, None, None]:
    create_db_and_tables(test_engine)
    with Session(test_engine) as session:
        create_first_user(session)
        yield session
        statement = delete(models.UsersTable)
        session.execute(statement)
        session.commit()


app.dependency_overrides[get_db_session] = override_get_db_session


@fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_first_user_token_headers(client)


# @fixture(scope="module")
# def normal_user_token_headers(client: TestClient, db: Session) -> dict[str, str]:
#    pass
