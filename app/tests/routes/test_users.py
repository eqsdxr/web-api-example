from fastapi.testclient import TestClient


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
