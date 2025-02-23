from fastapi.testclient import TestClient
from sqlmodel import Session

from app.crud import create_db_user, get_user_by_username
from app.config import main_config
from app.models import UserCreate


def test_read_users(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    response = client.get(url="api/users/", headers=superuser_token_headers)
    assert response.status_code == 200


def test_create_user(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    response = client.post(
        url="api/users/",
        json={
            "username": "adlkfjdafj",
            "password": "kljadskfoih",
        },
        headers=superuser_token_headers,
    )
    assert response.status_code == 200


def test_read_user_by_id(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    test_session: Session,
):
    user = get_user_by_username(test_session, main_config.first_user_username)
    assert user, "Error getting a first user by username"
    id = user.id
    response = client.get(
        url=f"api/users/{id}", headers=superuser_token_headers
    )
    assert response.status_code == 200


def test_update_user(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    test_session: Session,
):
    user = get_user_by_username(test_session, main_config.first_user_username)
    assert user, "Error getting a first user by username"
    id = user.id
    new_bio = "Test bio"
    response = client.patch(
        url=f"api/users/{id}",
        json={"bio": new_bio},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    assert response.json()["bio"] == new_bio


def test_delete_user(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    test_session: Session,
):
    created_user = create_db_user(
        test_session,
        UserCreate(username="DFLKJFijdf", password="KWLEFjkljdfj"),
    )
    assert created_user, "Error getting a first user by username"
    response = client.delete(
        url=f"api/users/{created_user.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
