import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from app.config import get_settings


@pytest.mark.anyio
async def test_login_access_token(app: FastAPI):
    data = {
        "grant_type": "password",
        "username": get_settings().FIRST_SUPERUSER_USERNAME,
        "password": get_settings().FIRST_SUPERUSER_PASSWORD,
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("api/v1/login/access-token", data=data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
