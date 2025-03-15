import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session, select

from app.crud import create_user
from app.models import User, UserCreate
from app.sec import verify_password


@pytest.mark.anyio
async def test_get_user_me(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert "id" in data and "username" in data
    assert "password_hash" not in data


@pytest.mark.anyio
async def test_get_users(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "users" in data


@pytest.mark.anyio
async def test_create_user(app: FastAPI):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "api/v1/users/",
            json={"username": "vampire999", "password": "dark_streets"},
        )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "vampire999"
    assert "id" in data


@pytest.mark.anyio
async def test_update_user(app: FastAPI, db_session: Session):
    user = create_user(
        db_session, UserCreate(username="human000", password="bright_days")
    )

    created_user = (
        db_session.exec(select(User).where(User.id == user.id))
        .one()
        .model_copy()
    )

    assert created_user
    assert created_user.username == "human000"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.patch(
            f"api/v1/users/{user.id}",
            json={"username": "vampire999", "password": "dark_streets"},
        )
    assert response.status_code == 202
    data = response.json()
    assert data["username"] == "vampire999"
    db_user = db_session.get(User, user.id)
    db_session.refresh(db_user)
    assert db_user
    assert db_user.hashed_password != created_user.hashed_password
    assert db_user.is_superuser is not True


@pytest.mark.anyio
async def test_update_user_me(
    app: FastAPI, db_session: Session, test_user: User
):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.patch(
            "api/v1/users/me",
            json={"username": "vampire999", "password": "dark_streets"},
        )
    assert response.status_code == 202
    db_session.refresh(test_user)
    assert test_user.username == "vampire999"
    assert verify_password("dark_streets", test_user.hashed_password)


@pytest.mark.anyio
async def test_delete_user(app: FastAPI, db_session: Session):
    user = create_user(
        db_session, UserCreate(username="human000", password="bright_days")
    )

    user_id = user.id  # Save id to check user when it's supposed to be deleted

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.delete(
            f"api/v1/users/{user.id}",
        )
    assert response.status_code == 202
    db_session.expire_all()
    deleted_user = db_session.get(User, user_id)
    assert deleted_user is None
