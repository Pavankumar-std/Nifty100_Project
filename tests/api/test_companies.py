from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)


def get_companies_list():
    """Get companies list regardless of API response structure."""

    response = client.get("/api/v1/companies")
    assert response.status_code == 200

    data = response.json()

    if isinstance(data, list):
        return data

    if isinstance(data, dict) and "companies" in data:
        return data["companies"]

    return []


def test_get_all_companies():
    response = client.get("/api/v1/companies")

    assert response.status_code == 200


def test_companies_returns_data():
    companies = get_companies_list()

    assert len(companies) > 0


def test_companies_count():
    companies = get_companies_list()

    assert len(companies) == 92


def test_company_has_required_fields():
    companies = get_companies_list()

    assert len(companies) > 0

    company = companies[0]

    assert "id" in company or "company_id" in company


def test_search_company():
    response = client.get(
        "/api/v1/companies",
        params={"search": "TCS"}
    )

    assert response.status_code == 200


def test_invalid_company():
    response = client.get(
        "/api/v1/companies/INVALID_COMPANY_XYZ"
    )

    assert response.status_code == 404