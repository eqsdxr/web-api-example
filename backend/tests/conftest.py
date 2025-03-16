from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlmodel import Session

from app.db import (
    engine,
)
from app.main import app as app
from tests.utils import get_superuser_token_headers, init_db


@fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@fixture(scope="function", autouse=True)
def db_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        session.commit()


@fixture(scope="function")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)
