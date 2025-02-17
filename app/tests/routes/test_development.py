from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import UsersTable


def test_check_api(client: TestClient):
    response = client.get("api/development/check-api")
    assert response.status_code == 200


def test_create_user(client: TestClient, db: Session) -> None:
    r = client.post(
        "api/development/create_superuser/",
        json={
            "email": "test@test.com",
            "username": "testtest",
            "password": "password",
        },
    )

    assert r.status_code == 200
    data = r.json()
    user = db.exec(select(UsersTable).where(UsersTable.id == data["id"])).first()
    assert user
    assert user.email == "test@test.com"
    assert user.username == "testtest"
