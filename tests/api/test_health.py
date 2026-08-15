from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_health_status_code():
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_health_status():
    response = client.get("/api/v1/health")
    data = response.json()

    assert data["status"] == "ok"


def test_health_has_version():
    response = client.get("/api/v1/health")
    data = response.json()

    assert "version" in data


def test_health_has_uptime():
    response = client.get("/api/v1/health")
    data = response.json()

    assert "uptime_seconds" in data


def test_health_has_db_counts():
    response = client.get("/api/v1/health")
    data = response.json()

    assert "db_row_counts" in data


def test_health_companies_count():
    response = client.get("/api/v1/health")
    data = response.json()

    assert data["db_row_counts"]["companies"] == 92