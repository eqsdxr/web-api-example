from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import User


def test_create_user_private(db_session: Session, client: TestClient) -> None:
    response = client.post(
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
