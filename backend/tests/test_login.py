from fastapi.testclient import TestClient

from app.config import get_settings


def test_login_access_token(client: TestClient):
    data = {
        "grant_type": "password",
        "username": get_settings().FIRST_SUPERUSER_USERNAME,
        "password": get_settings().FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post("api/v1/login/access-token", data=data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
