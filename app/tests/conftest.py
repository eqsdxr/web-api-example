from fastapi import FastAPI
from pytest import fixture

from ..main import app as main_app


@fixture(scope="module")
async def app() -> FastAPI:
    return main_app
