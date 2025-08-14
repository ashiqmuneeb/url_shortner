import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    init_db()

client = TestClient(app)

def test_health():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_shorten_and_redirect():
    payload = {"url": "https://example.com/path?x=1"}
    r = client.post("/api/shorten", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "code" in data and "short_url" in data

    code = data["code"]
    # expand
    r2 = client.get(f"/api/expand/{code}")
    assert r2.status_code == 200
    assert r2.json()["original_url"] == payload["url"]

    # redirect
    r3 = client.get(f"/{code}", allow_redirects=False)
    assert r3.status_code in (301, 302, 307)
    assert r3.headers["location"].startswith("https://example.com")
