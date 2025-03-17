from fastapi.testclient import TestClient


def test_get_items(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    response = client.post(
        "api/v1/items/",
        json={"title": "fallen star"},
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    created_item_data = response.json()
    assert "id" in created_item_data
    response = client.get("api/v1/items/", headers=superuser_token_headers)
    get_item_data = response.json()
    assert len(get_item_data["data"]) == 1
    assert get_item_data["data"][0]["title"] == "fallen star"
