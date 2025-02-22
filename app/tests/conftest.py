from collections.abc import Generator

from fastapi.testclient import TestClient
from pytest import fixture
from sqlmodel import Session, delete

from app.main import app
from app.tests.utils import get_first_user_token_headers
from app.db import engine, init_db
from app import models


@fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:  # Use for direct db operations
    with Session(engine) as session:
        init_db(engine, create_superuser=True)
        yield session
        statement = delete(models.UsersTable)
        session.execute(statement)
        session.commit()


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
