from fastapi.testclient import TestClient

def test_check_api(client: TestClient):
    response = client.get("api/development/check")
    assert response.status_code == 200

