from collections.abc import Generator

from pytest import fixture
from fastapi.testclient import TestClient
from sqlalchemy import Connection

from app.main import app


@fixture(scope="session")
def db() -> Generator[Connection, None, None]:
    with Connection(engine) as conn:  # TODO - Which engine should I put here?
        # init_db(session)
        yield session


@fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
