from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_scan_file():
    response = client.post(
        "/api/v1/pii/scan",
        files={"file": ("test.txt", b"sample content")},
    )
    assert response.status_code == 200
    assert "pii_found" in response.json()
