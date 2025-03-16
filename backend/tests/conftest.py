from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlmodel import Session

from app.db import (
    create_first_superuser_if_doesnt_exist,
    create_tables,
    engine,
)
from app.deps import get_db
from app.main import app as app
from tests.utils import get_superuser_token_headers


@fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


def get_test_db() -> Generator[Session, None, None]:
    create_tables(engine)
    with Session(engine) as session:
        create_first_superuser_if_doesnt_exist(session)
        yield session
        session.commit()


@fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    yield from get_test_db()


app.dependency_overrides[get_db] = get_test_db


@fixture(scope="function")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)
