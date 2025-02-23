from fastapi.testclient import TestClient

def test_upload(client: TestClient):
    get_response = client.get(
        "/upload"
    )
    assert get_response != 200

    with open("tests/static/test.jpg", "rb") as file:
        post_response = client.post("/upload", files={"file": file})
    assert post_response.status_code == 200
    data = post_response.json()
    assert "filename" in data
    assert "metadata" in data
    assert data["type"] == "image/jpeg"
