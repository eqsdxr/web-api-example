from collections.abc import Generator

from pytest import fixture
from fastapi.testclient import TestClient

from app.main import app

@fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c

