import pytest
from src.etl.normaliser import normalize_year, normalize_ticker


# -----------------------
# normalize_year() Tests
# -----------------------

def test_year_string():
    assert normalize_year("2024") == 2024


def test_year_integer():
    assert normalize_year(2023) == 2023


def test_year_none():
    assert normalize_year(None) is None


def test_year_empty():
    assert normalize_year("") is None


def test_year_invalid():
    assert normalize_year("abcd") is None


def test_year_float():
    assert normalize_year(2024.0) == 2024


def test_year_spaces():
    assert normalize_year(" 2022 ") == 2022


def test_year_zero():
    assert normalize_year(0) == 0


def test_year_negative():
    assert normalize_year(-1) == -1


def test_year_large():
    assert normalize_year(9999) == 9999


def test_year_invalid_text():
    assert normalize_year("year") is None


def test_year_special():
    assert normalize_year("@@@") is None


def test_year_bool():
    assert normalize_year(True) == 1


def test_year_false():
    assert normalize_year(False) == 0


def test_year_whitespace():
    assert normalize_year("   ") is None


# -------------------------
# normalize_ticker() Tests
# -------------------------

def test_ticker_upper():
    assert normalize_ticker("TCS") == "TCS"


def test_ticker_lower():
    assert normalize_ticker("tcs") == "TCS"


def test_ticker_spaces():
    assert normalize_ticker(" tcs ") == "TCS"


def test_ticker_mixed():
    assert normalize_ticker("InFoSyS") == "INFOSYS"


def test_ticker_none():
    assert normalize_ticker(None) is None


def test_ticker_empty():
    assert normalize_ticker("") == ""


def test_ticker_numbers():
    assert normalize_ticker("abc123") == "ABC123"


def test_ticker_symbol():
    assert normalize_ticker("m&m") == "M&M"


def test_ticker_dash():
    assert normalize_ticker("bajaj-auto") == "BAJAJ-AUTO"


def test_ticker_spaces_inside():
    assert normalize_ticker("hdfc bank") == "HDFC BANK"