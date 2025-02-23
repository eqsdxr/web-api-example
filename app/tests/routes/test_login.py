from fastapi.testclient import TestClient

from app.config import main_config


def test_login(client: TestClient) -> None:
    login_data = {
        "username": main_config.first_user_username,
        "password": main_config.first_user_password,
    }
    response = client.post("api/login/access-token", data=login_data)
    tokens = response.json()
    assert response.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]
