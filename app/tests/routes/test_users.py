from fastapi.testclient import TestClient


def test_create_users(client: TestClient):
    response = client.post(
        url="api/users/",
        json={
            "email": "test@test.com",
            "username": "testusername",
            "password": "testtest",
        },
    )
    assert response.status_code == 200
