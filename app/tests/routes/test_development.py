from fastapi.testclient import TestClient


def test_check_api(client: TestClient):
    response = client.get("api/development/check-api")
    assert response.status_code == 200


def test_check_database_connection(client: TestClient):
    r = client.get(
        "api/development/check-db",
    )
    assert r.status_code == 200


def test_create_user_dev(client: TestClient) -> None:
    r = client.post(
        "api/development/create-user-dev/",
        json={
            "username": "DSF(*J#jfdsfkjh",
            "password": "password",
        },
    )

    assert r.status_code == 200
