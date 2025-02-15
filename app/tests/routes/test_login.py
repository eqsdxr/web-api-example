from fastapi.testclient import TestClient


def test_login(client: TestClient):
    response = client.get("api/login/")
