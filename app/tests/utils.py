import random
import string

from fastapi.testclient import TestClient

from app.config import main_config


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_first_user_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "email": main_config.first_user_email,
        "username": main_config.first_user_username,
        "password": main_config.first_user_password,
    }
    r = client.post("api/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
