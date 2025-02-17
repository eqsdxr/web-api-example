from collections.abc import Generator

from pytest import fixture
from sqlmodel import Session
from fastapi.testclient import TestClient

from app.db import engine
from app.main import app
from app.tests.utils import get_first_user_token_headers


@fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


@fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_first_user_token_headers(client)

