import os


def test_data_folder_exists():
    assert os.path.exists("data")


def test_companies_file_exists():
    assert os.path.exists("data/companies.xlsx")


def test_profit_file_exists():
    assert os.path.exists("data/profitandloss.xlsx")


def test_balance_file_exists():
    assert os.path.exists("data/balancesheet.xlsx")


def test_cashflow_file_exists():
    assert os.path.exists("data/cashflow.xlsx")


def test_database_folder_exists():
    assert os.path.exists("db")


def test_schema_exists():
    assert os.path.exists("db/schema.sql")


def test_output_folder_exists():
    assert os.path.exists("output")