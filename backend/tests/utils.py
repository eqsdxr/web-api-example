from fastapi.testclient import TestClient
from app.config import get_settings


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": get_settings().FIRST_SUPERUSER_USERNAME,
        "password": get_settings().FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("api/v1/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
