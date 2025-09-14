from fastapi.testclient import TestClient
from api.main import app
client = TestClient(app) # A special client for testing our API.
# A test is just a function that starts with 'test_'.
def test_health():
    # Make a fake request to the /health endpoint.
    r = client.get("/health")
    # 'assert' checks if a condition is true. If not, the test fails.
    # Here, we check that the server responded with "200 OK".
    assert r.status_code == 200
def test_scan_text_endpoint():
    # Make a fake POST request with some text containing an email.
    r = client.post("/api/v1/scan/text", json={"text":"reach me at test@example.com"})
    assert r.status_code == 200
    data = r.json()
    # Check that the scanner found at least one secret.
    assert data["count"] >= 1