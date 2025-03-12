import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@pytest.mark.anyio
async def test_get_user_me(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data and "username" in data
    assert not "password_hash" in data
