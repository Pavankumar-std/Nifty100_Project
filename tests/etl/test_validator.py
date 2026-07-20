import pandas as pd


def test_company_id_unique():
    df = pd.read_excel("data/companies.xlsx", header=1)
    assert "id" in df.columns


def test_company_name_exists():
    df = pd.read_excel("data/companies.xlsx", header=1)
    assert "company_name" in df.columns


def test_profit_company_id_exists():
    df = pd.read_excel("data/profitandloss.xlsx", header=1)
    assert "company_id" in df.columns


def test_profit_year_exists():
    df = pd.read_excel("data/profitandloss.xlsx", header=1)
    assert "year" in df.columns


def test_sales_column_exists():
    df = pd.read_excel("data/profitandloss.xlsx", header=1)
    assert "sales" in df.columns


def test_balance_assets_exists():
    df = pd.read_excel("data/balancesheet.xlsx", header=1)
    assert "total_assets" in df.columns


def test_balance_liabilities_exists():
    df = pd.read_excel("data/balancesheet.xlsx", header=1)
    assert "total_liabilities" in df.columns


def test_cashflow_exists():
    df = pd.read_excel("data/cashflow.xlsx", header=1)
    assert len(df) > 0