from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import DEFAULT_TOKEN, DEFAULT_X_TOKEN

client = TestClient(app)


def test_read_users():
    response = client.get("/users", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": 200000,
        "message": "API response success",
        "result": [
            {"username": "Rick"},
            {"username": "Morty"}
        ]
    }

def test_read_user_me():
    response = client.get("/users/me", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": 200000,
        "message": "API response success",
        "result": {
            "username": "fakecurrentuser"
        }
    }

def test_read_user():
    user_name = "sally"
    response = client.get(f"/users/{user_name}", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": 200000,
        "message": "API response success",
        "result": {
            "username": "sally"
        }
    }