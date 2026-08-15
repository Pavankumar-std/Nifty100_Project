import pandas as pd


# -----------------------------------
# Simple Data Quality Rule Functions
# -----------------------------------

def check_missing_company_id(df):
    return bool(df["company_id"].isna().any())


def check_duplicate_company_id(df):
    return bool(df["company_id"].duplicated().any())


def check_negative_sales(df):
    return bool((df["sales"] < 0).any())


def check_missing_year(df):
    return bool(df["year"].isna().any())


def check_invalid_year(df):
    years = pd.to_numeric(df["year"], errors="coerce")
    return bool(years.isna().any())


def check_negative_profit(df):
    return bool((df["net_profit"] < 0).any())


def check_missing_ticker(df):
    return bool(df["ticker"].isna().any())


def check_duplicate_ticker(df):
    return bool(df["ticker"].duplicated().any())


def check_negative_assets(df):
    return bool((df["assets"] < 0).any())


def check_negative_equity(df):
    return bool((df["equity"] < 0).any())


def check_missing_sector(df):
    return bool(df["sector"].isna().any())


def check_zero_company_id(df):
    return bool((df["company_id"] == 0).any())


def check_empty_company_name(df):
    return bool((df["company_name"].fillna("") == "").any())


def check_invalid_ticker(df):
    return bool(df["ticker"].astype(str).str.strip().eq("").any())


# -----------------------------------
# Tests
# -----------------------------------

def test_missing_company_id():
    df = pd.DataFrame({"company_id": [1, None]})
    assert check_missing_company_id(df) is True


def test_duplicate_company_id():
    df = pd.DataFrame({"company_id": [1, 1]})
    assert check_duplicate_company_id(df) is True


def test_negative_sales():
    df = pd.DataFrame({"sales": [100, -50]})
    assert check_negative_sales(df) is True


def test_missing_year():
    df = pd.DataFrame({"year": [2023, None]})
    assert check_missing_year(df) is True


def test_invalid_year():
    df = pd.DataFrame({"year": ["2023", "abcd"]})
    assert check_invalid_year(df) is True


def test_negative_profit():
    df = pd.DataFrame({"net_profit": [100, -10]})
    assert check_negative_profit(df) is True


def test_missing_ticker():
    df = pd.DataFrame({"ticker": ["TCS", None]})
    assert check_missing_ticker(df) is True


def test_duplicate_ticker():
    df = pd.DataFrame({"ticker": ["TCS", "TCS"]})
    assert check_duplicate_ticker(df) is True


def test_negative_assets():
    df = pd.DataFrame({"assets": [1000, -1]})
    assert check_negative_assets(df) is True


def test_negative_equity():
    df = pd.DataFrame({"equity": [500, -10]})
    assert check_negative_equity(df) is True


def test_missing_sector():
    df = pd.DataFrame({"sector": ["IT", None]})
    assert check_missing_sector(df) is True


def test_zero_company_id():
    df = pd.DataFrame({"company_id": [1, 0]})
    assert check_zero_company_id(df) is True


def test_empty_company_name():
    df = pd.DataFrame({"company_name": ["TCS", ""]})
    assert check_empty_company_name(df) is True


def test_invalid_ticker():
    df = pd.DataFrame({"ticker": ["TCS", "   "]})
    assert check_invalid_ticker(df) is True