from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def test_screener_status():
    response = client.get("/api/v1/screener")
    assert response.status_code == 200


def test_screener_returns_data():
    response = client.get("/api/v1/screener")
    data = response.json()

    assert len(data) > 0


def test_screener_min_roe():
    response = client.get(
        "/api/v1/screener",
        params={"min_roe": 15}
    )

    assert response.status_code == 200


def test_screener_max_de():
    response = client.get(
        "/api/v1/screener",
        params={"max_de": 1}
    )

    assert response.status_code == 200


def test_screener_sector():
    response = client.get(
        "/api/v1/screener",
        params={"sector": "IT"}
    )

    assert response.status_code == 200


def test_screener_invalid_parameter():
    response = client.get(
        "/api/v1/screener",
        params={"min_roe": -10}
    )

    assert response.status_code == 400