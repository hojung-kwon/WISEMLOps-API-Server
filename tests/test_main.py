from fastapi.testclient import TestClient

from src.dependencies import DEFAULT_TOKEN, DEFAULT_X_TOKEN
from src.main import app

client = TestClient(app)


def test_root():
    response = client.get("/", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json()["title"] == app.title
    assert response.json()["description"] == app.description
    assert response.json()["version"] == app.version
    assert response.json()["docs_url"] == app.docs_url


def test_health():
    response = client.get("/health", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}