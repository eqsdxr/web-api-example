import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.config import get_settings


@pytest.mark.anyio
async def test_upload_single_img(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        get_response = await ac.get("/upload")
    assert get_response.status_code != 200

    test_image = get_settings().test_static_dir / "test_img1.jpg"
    with open(test_image, "rb") as file:
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            post_response = await ac.post("/upload", files={"files": file})

    assert post_response.status_code == 200
    data = post_response.json()
    assert "metadata_set" in data
    assert "count" in data
    assert len(data["metadata_set"]) == 1
    assert "filename" in data["metadata_set"][0]
    assert "metadata" in data["metadata_set"][0]
    assert data["metadata_set"][0]["content_type"] == "image/jpeg"


@pytest.mark.anyio
async def test_upload_multiple_imgs(app: FastAPI):
    test_dir = get_settings().test_static_dir
    imgs = ["test_img1.jpg", "test_img2.jpg"]

    files = []
    for img in imgs:
        img_path = test_dir / img
        files.append(("files", (img, img_path.read_bytes(), "image/jpeg")))

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/upload", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert "metadata_set" in data
    assert len(data["metadata_set"]) == 2


@pytest.mark.anyio
async def test_login_access_token(app: FastAPI):
    data = {
        "grant_type": "password",
        "username": get_settings().first_superuser_username,
        "password": get_settings().first_superuser_password,
    }
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post("/login/access-token", data=data)

    assert response.status_code == 200
    data = response.json()
