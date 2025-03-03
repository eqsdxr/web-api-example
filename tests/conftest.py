from typing import Annotated, Generator

from fastapi import Depends, FastAPI
from pytest import fixture
from sqlmodel import Session

from app.db import create_first_user, create_tables, engine
from app.deps import get_db
from app.main import app as main_app


@fixture(scope="module")
async def app() -> FastAPI:
    return main_app


def get_test_db() -> Generator[Session, None, None]:
    create_tables(engine)
    with Session(engine) as session:
        create_first_user(session)
        yield session
        session.commit()


TestDBSessionDep = Annotated[Session, Depends(get_test_db)]

main_app.dependency_overrides[get_db] = get_test_db
