import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


@pytest.mark.anyio
async def test_upload(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        get_response = await ac.get("/upload")
    assert get_response.status_code != 200

    test_image = "backend/tests/static/test.jpg"
    with open(test_image, "rb") as file:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_response = await ac.post("/upload", files={"file": file})

    assert post_response.status_code == 200
    data = post_response.json()
    assert "filename" in data
    assert "metadata" in data
    assert data["type"] == "image/jpeg"
