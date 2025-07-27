from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Backend is running"}

def test_register_user():
    payload = {"email": "testuser@example.com", "password": "strongpassword"}
    response = client.post("/register", json=payload)
    assert response.status_code == 200 or response.status_code == 400

def test_login():
    payload = {"email": "testuser@example.com", "password": "strongpassword"}
    response = client.post("/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_calculate_tax():
    payload = {"income": 600000}
    response = client.post("/calculate-tax", json=payload)
    assert response.status_code == 200
    assert "tax" in response.json()
