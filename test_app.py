import pytest # type: ignore
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"hello from cicd-demo" in res.data

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert b"true" in res.data.lower()