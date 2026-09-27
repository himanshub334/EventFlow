from fastapi.testclient import TestClient
from app.main import app

client=TestClient(app)

def test_openapi():
    r=client.get("/openapi.json")
    assert r.status_code==200
    assert "/events" in r.json()["paths"]

def test_context():
    r=client.get("/mock/context?campaign_id=c1")
    assert r.status_code==200
    assert r.json()["campaign_id"]=="c1"
