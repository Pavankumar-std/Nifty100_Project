import pytest


# -----------------------------
# ROE Tests
# -----------------------------

def calculate_roe(net_profit, equity):
    if equity is None or equity <= 0:
        return None
    return round((net_profit / equity) * 100, 2)


def test_roe_positive_equity():
    assert calculate_roe(100, 500) == 20.0


def test_roe_zero_equity():
    assert calculate_roe(100, 0) is None


def test_roe_negative_equity():
    assert calculate_roe(100, -500) is None


def test_roe_zero_profit():
    assert calculate_roe(0, 500) == 0.0


def test_roe_negative_profit():
    assert calculate_roe(-100, 500) == -20.0


# -----------------------------
# Debt to Equity Tests
# -----------------------------

def calculate_debt_equity(debt, equity):
    if equity is None or equity == 0:
        return None
    return round(debt / equity, 2)


def test_debt_free_company():
    assert calculate_debt_equity(0, 500) == 0.0


def test_normal_debt_equity():
    assert calculate_debt_equity(200, 400) == 0.5


def test_high_debt_equity():
    assert calculate_debt_equity(3000, 500) == 6.0


def test_zero_equity_debt_equity():
    assert calculate_debt_equity(100, 0) is None


# -----------------------------
# Interest Coverage Tests
# -----------------------------

def calculate_icr(operating_profit, interest):
    if interest is None or interest == 0:
        return None
    return round(operating_profit / interest, 2)


def test_normal_interest_coverage():
    assert calculate_icr(500, 100) == 5.0


def test_zero_interest():
    assert calculate_icr(500, 0) is None


def test_negative_operating_profit():
    assert calculate_icr(-100, 50) == -2.0


# -----------------------------
# CAGR Tests
# -----------------------------

def calculate_cagr(start_value, end_value, years):
    if (
        start_value is None
        or end_value is None
        or years is None
        or start_value <= 0
        or years <= 0
    ):
        return None

    return round(
        ((end_value / start_value) ** (1 / years) - 1) * 100,
        2
    )


def test_normal_cagr():
    assert calculate_cagr(100, 200, 5) == 14.87


def test_zero_start_value():
    assert calculate_cagr(0, 200, 5) is None


def test_negative_start_value():
    assert calculate_cagr(-100, 200, 5) is None


def test_zero_years():
    assert calculate_cagr(100, 200, 0) is None


def test_cagr_decline():
    assert calculate_cagr(200, 100, 5) == -12.94


# -----------------------------
# Flag Tests
# -----------------------------

def high_leverage_flag(debt_to_equity):
    if debt_to_equity is None:
        return False
    return debt_to_equity > 5


def test_high_leverage_flag_true():
    assert high_leverage_flag(6) is True


def test_high_leverage_flag_false():
    assert high_leverage_flag(2) is False


def test_high_leverage_boundary():
    assert high_leverage_flag(5) is False