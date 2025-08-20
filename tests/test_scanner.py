from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_scan_file():
	response = client.post(
		"/scan",
		files={"file": ("test.txt", b"sample content")},
	)
	assert response.status_code == 200
	assert "pii_found" in response.json()
