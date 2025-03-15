from typing import Annotated, Generator

from fastapi import Depends, FastAPI
from pytest import fixture
from sqlmodel import Session, select

from app.config import get_settings
from app.db import (
    create_first_superuser_if_doesnt_exist,
    create_tables,
    engine,
)
from app.deps import get_current_user, get_db
from app.main import app as main_app
from app.models import User


@fixture(scope="module")
async def app() -> FastAPI:
    return main_app


def get_test_db() -> Generator[Session, None, None]:
    create_tables(engine)
    with Session(engine) as session:
        create_first_superuser_if_doesnt_exist(session)
        yield session
        session.commit()


@fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    yield from get_test_db()


main_app.dependency_overrides[get_db] = get_test_db

TestDBSessionDep = Annotated[Session, Depends(get_test_db)]


def get_test_current_user(session: TestDBSessionDep) -> User:
    user = session.exec(
        select(User).where(
            User.username == get_settings().FIRST_SUPERUSER_USERNAME
        )
    ).first()
    if not user:
        raise ValueError("No test user found in database")
    return user


main_app.dependency_overrides[get_current_user] = get_test_current_user


@fixture(scope="function")
def test_user(db_session: TestDBSessionDep) -> User:
    return get_test_current_user(db_session)
