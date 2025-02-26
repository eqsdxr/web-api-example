from fastapi import FastAPI
from pytest import fixture

from app.main import app as main_app


@fixture(scope="module")
async def app() -> FastAPI:
    return main_app
