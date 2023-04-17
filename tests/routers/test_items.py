from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import DEFAULT_TOKEN, DEFAULT_X_TOKEN

client = TestClient(app)


def test_read_items():
    response = client.get("/items", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": 200000,
        "message": "API response success",
        "result": {
            "plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}
        }
    }


def test_read_item():
    item_id = "gun"
    response = client.get(f"/items/{item_id}", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": 200000,
        "message": "API response success",
        "result": {
            "name": "Portal Gun",
            "item_id": "gun"
        }
    }


def test_update_item():
    item_id = "plumbus"
    response = client.put(f"/items/{item_id}", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": 200000,
        "message": "API response success",
        "result": {
            "item_id": "plumbus",
            "name": "The great Plumbus"
        }
    }


def test_create_item():
    item = {
        "name": "apple",
        "status": "in stock",
        "stock": 10
    }
    response = client.post(url="/items", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN}, json=item)
    assert response.status_code == 200
    assert response.json()["result"]["item"]["name"] == item["name"]
    assert response.json()["result"]["item"]["status"] == item["status"]
    assert response.json()["result"]["item"]["stock"] == item["stock"]
