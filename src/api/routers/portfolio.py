import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import APIRouter

router = APIRouter(
    prefix="/portfolio",
    tags=["Portfolio"]
)

BASE_DIR = Path(__file__).resolve().parents[3]
DB = BASE_DIR / "db" / "nifty100.db"


def get_connection():
    """Create SQLite database connection."""
    return sqlite3.connect(DB)


def clean_columns(df):
    """Clean dataframe column names."""
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


@router.get("/stats")
def get_portfolio_stats():
    """Return portfolio percentile statistics."""

    conn = get_connection()

    try:
        ratios = pd.read_sql(
            'SELECT * FROM "financial_ratios"',
            conn
        )
    finally:
        conn.close()

    ratios = clean_columns(ratios)

    # Get latest record for each company
    ratios["_year_num"] = (
        ratios["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    ratios["_year_num"] = pd.to_numeric(
        ratios["_year_num"],
        errors="coerce"
    )

    ratios = ratios.sort_values("_year_num")

    latest = (
        ratios.groupby("company_id")
        .tail(1)
        .copy()
    )

    # Available KPI columns
    possible_kpis = [
        "roe",
        "roce",
        "roa",
        "debt_to_equity",
        "net_profit_margin",
        "operating_profit_margin",
        "interest_coverage",
        "asset_turnover",
        "eps_ratio",
        "dividend_payout_ratio"
    ]

    kpis = [
        col for col in possible_kpis
        if col in latest.columns
    ]

    results = []

    for kpi in kpis:

        values = pd.to_numeric(
            latest[kpi],
            errors="coerce"
        ).dropna()

        if values.empty:
            continue

        results.append({
            "kpi": kpi,
            "p10": round(values.quantile(0.10), 2),
            "p25": round(values.quantile(0.25), 2),
            "p50": round(values.quantile(0.50), 2),
            "p75": round(values.quantile(0.75), 2),
            "p90": round(values.quantile(0.90), 2),
            "mean": round(values.mean(), 2),
            "std": round(values.std(), 2)
        })

    return {
        "company_count": int(latest["company_id"].nunique()),
        "statistics": results
    }