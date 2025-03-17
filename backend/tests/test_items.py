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


def test_update_item(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    create_response = client.post(
        "api/v1/items/",
        json={"title": "pretty picture"},
        headers=superuser_token_headers,
    )
    assert create_response.status_code == 200
    create_data = create_response.json()
    assert create_data["title"] == "pretty picture"
    assert create_data["id"]
    update_response = client.patch(
        f"api/v1/items/{create_data['id']}",
        json={"title": "ugly picture"},
        headers=superuser_token_headers,
    )
    assert update_response.status_code == 200
    update_data = update_response.json()
    assert update_data["title"] == "ugly picture"
