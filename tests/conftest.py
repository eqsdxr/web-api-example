from typing import Annotated, Generator

from fastapi import Depends, FastAPI
from pytest import fixture
from sqlmodel import Session, create_engine

from app.db import create_first_user, create_tables
from app.deps import get_db
from app.main import app as main_app


@fixture(scope="module")
async def app() -> FastAPI:
    return main_app


def get_test_db() -> Generator[Session, None, None]:
    test_engine = create_engine("sqlite:///sqlite.db")
    create_tables(test_engine)
    with Session(test_engine) as session:
        create_first_user(session)
        yield session


TestDBSessionDep = Annotated[Session, Depends(get_test_db)]

main_app.dependency_overrides[get_db] = get_test_db
