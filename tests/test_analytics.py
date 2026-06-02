from app.main import app
from fastapi.testclient import TestClient
client = TestClient(app)
def test_analytics():
    response = client.get("/analytics")
    assert response.status_code == 200
    assert "total_users" in response.json()
    assert "total_transactions" in response.json()