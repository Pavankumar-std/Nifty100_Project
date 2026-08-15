from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_sectors_status():
    response = client.get("/api/v1/sectors")
    assert response.status_code == 200


def test_sectors_returns_data():
    response = client.get("/api/v1/sectors")
    data = response.json()

    if isinstance(data, dict) and "sectors" in data:
        data = data["sectors"]

    assert len(data) > 0


def test_sectors_count():
    response = client.get("/api/v1/sectors")
    data = response.json()

    if isinstance(data, dict) and "sectors" in data:
        data = data["sectors"]

    assert len(data) > 0


def test_sector_companies():
    response = client.get("/api/v1/sectors/IT/companies")

    assert response.status_code in [200, 404]


def test_invalid_sector():
    response = client.get(
        "/api/v1/sectors/INVALID_SECTOR_XYZ/companies"
    )

    assert response.status_code == 404