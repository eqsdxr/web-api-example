from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Item


def test_get_items(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    created_response = client.post(
        "api/v1/items/",
        json={"title": "fallen star"},
        headers=superuser_token_headers,
    )
    assert created_response.status_code == 201
    created_item_data = created_response.json()
    assert "id" in created_item_data
    get_response = client.get("api/v1/items/", headers=superuser_token_headers)
    get_item_data = get_response.json()
    assert len(get_item_data["data"]) == 1
    assert get_item_data["data"][0]["title"] == "fallen star"


def test_get_item(client: TestClient, superuser_token_headers: dict[str, str]):
    create_response = client.post(
        "api/v1/items/",
        json={"title": "cool song"},
        headers=superuser_token_headers,
    )
    assert create_response.status_code == 201
    create_data = create_response.json()
    assert create_data["title"] == "cool song"
    assert create_data["id"]
    get_response = client.get(
        f"api/v1/items/{create_data['id']}",
        headers=superuser_token_headers,
    )
    assert get_response.status_code == 200
    get_data = get_response.json()
    assert get_data["title"] == "cool song"


def test_create_item(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    create_response = client.post(
        "api/v1/items/",
        json={
            "title": "good code",
            "description": "It was me who wrote that.",
        },
        headers=superuser_token_headers,
    )
    assert create_response.status_code == 201
    create_data = create_response.json()
    assert create_data["title"] == "good code"
    assert create_data["description"] == "It was me who wrote that."
    assert create_data["id"]


def test_update_item(
    client: TestClient, superuser_token_headers: dict[str, str]
):
    create_response = client.post(
        "api/v1/items/",
        json={"title": "pretty picture"},
        headers=superuser_token_headers,
    )
    assert create_response.status_code == 201
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


def test_delete_item(
    client: TestClient,
    superuser_token_headers: dict[str, str],
    db_session: Session,
):
    create_response = client.post(
        "api/v1/items/",
        json={"title": "picture of dawn"},
        headers=superuser_token_headers,
    )
    assert create_response.status_code == 201
    create_data = create_response.json()
    assert create_data["title"] == "picture of dawn"
    assert create_data["id"]
    deleted_response = client.delete(
        f"api/v1/items/{create_data['id']}",
        headers=superuser_token_headers,
    )
    assert deleted_response.status_code == 200
    deleted_item = db_session.get(Item, create_data["id"])
    assert deleted_item is None
