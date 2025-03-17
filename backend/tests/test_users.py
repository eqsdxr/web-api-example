from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.crud import create_user
from app.models import User, UserCreate
from app.sec import verify_password


def test_get_user_me(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    response = client.get("api/v1/users/me", headers=superuser_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data and "username" in data
    assert "password_hash" not in data


def test_get_users(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    response = client.get("api/v1/users/", headers=superuser_token_headers)
    assert response.status_code == 200
    data = response.json()
    assert "count" in data
    assert "users" in data


def test_create_user(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    response = client.post(
        "api/v1/users/",
        json={"username": "vampire999", "password": "dark_streets"},
        headers=superuser_token_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "vampire999"
    assert "id" in data


def test_update_user(
    client: TestClient,
    db_session: Session,
    superuser_token_headers: dict[str, str],
):
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

    response = client.patch(
        f"api/v1/users/{user.id}",
        json={"username": "vampire999", "password": "dark_streets"},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "vampire999"
    db_user = db_session.get(User, user.id)
    db_session.refresh(db_user)
    assert db_user
    assert db_user.hashed_password != created_user.hashed_password
    assert db_user.is_superuser is not True


def test_update_user_me(
    client: TestClient,
    db_session: Session,
    superuser_token_headers: dict[str, str],
):
    response = client.patch(
        "api/v1/users/me",
        json={"username": "vampire999", "password": "dark_streets"},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "vampire999"
    user = db_session.exec(select(User).where(User.id == data["id"])).one()
    assert verify_password("dark_streets", user.hashed_password)


def test_delete_user(
    client: TestClient,
    db_session: Session,
    superuser_token_headers: dict[str, str],
):
    user = create_user(
        db_session, UserCreate(username="human000", password="bright_days")
    )

    user_id = user.id  # Save id to check user when it's supposed to be deleted

    response = client.delete(
        f"api/v1/users/{user.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    db_session.expire_all()
    deleted_user = db_session.get(User, user_id)
    assert deleted_user is None
