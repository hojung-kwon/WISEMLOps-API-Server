from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import DEFAULT_TOKEN, DEFAULT_X_TOKEN

client = TestClient(app)


def test_update_admin():
    response = client.post(url="/admin", params={"token": DEFAULT_TOKEN}, headers={"x-token": DEFAULT_X_TOKEN})
    assert response.status_code == 200
    assert response.json() == {
        "code": 200000,
        "message": "API response success",
        "result": "Admin getting schwifty"
    }