import pytest
from app.models import User
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlmodel import Session, select


@pytest.mark.anyio
async def test_create_user_private(db_session: Session, app: FastAPI) -> None:
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.post(
            "api/v1/private/create-user",
            json={
                "username": "vampire",
                "password": "beautifulnight",
            },
        )
    assert response.status_code == 200
    data = response.json()
    user = db_session.exec(select(User).where(User.id == data["id"])).one()
    assert user.is_active
    assert not user.is_superuser
    assert user.username == "vampire"
    assert user.hashed_password
