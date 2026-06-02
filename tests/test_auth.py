from app.main import app
import uuid
from fastapi.testclient import TestClient

client = TestClient(app)

def test_register_user():
    #Generate random email
    unique_email = f"test_{uuid.uuid4().hex[:8]}@gmail.com"

    response = client.post(
        "/register", json={
            "email": unique_email,
            "password":"pg123"
        }
    )
    assert response.status_code == 201