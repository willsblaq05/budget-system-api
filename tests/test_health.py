from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_healht():
    response = client.get("/health") 
    
    assert response.status_code == 200
    assert response.json() == {"Message":"Finance API is running"}