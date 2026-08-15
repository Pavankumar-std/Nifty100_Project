import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/market-cap",
    tags=["Market Cap & Valuation"]
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


@router.get("/{ticker}")
def get_market_cap_history(ticker: str):
    """Return historical market cap and valuation data."""

    conn = get_connection()

    try:
        market_cap = pd.read_sql(
            'SELECT * FROM "market cap"',
            conn
        )

        companies = pd.read_sql(
            'SELECT * FROM "companies"',
            conn
        )

    finally:
        conn.close()

    market_cap = clean_columns(market_cap)
    companies = clean_columns(companies)

    # Make sure company_id is available
    if "id" in companies.columns and "company_id" not in companies.columns:
        companies["company_id"] = companies["id"]

    companies["company_id"] = companies["company_id"].astype(str)

    if "company_id" in market_cap.columns:
        market_cap["company_id"] = market_cap["company_id"].astype(str)
    else:
        raise HTTPException(
            status_code=500,
            detail="company_id column not found in market cap table"
        )

    # Find ticker/company match
    ticker_col = None

    for col in ["ticker", "symbol", "company_name"]:
        if col in companies.columns:
            ticker_col = col
            break

    if ticker_col is None:
        raise HTTPException(
            status_code=500,
            detail="Ticker column not found"
        )

    company = companies[
        companies[ticker_col]
        .astype(str)
        .str.lower()
        == ticker.lower()
    ]

    if company.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Company '{ticker}' not found"
        )

    company_id = str(company.iloc[0]["company_id"])

    result = market_cap[
        market_cap["company_id"] == company_id
    ].copy()

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No market cap data found for '{ticker}'"
        )

    # Sort by year if available
    if "year" in result.columns:
        result = result.sort_values("year")

    result = result.where(
        pd.notnull(result),
        None
    )

    return {
        "ticker": ticker,
        "company_id": company_id,
        "records": result.to_dict(
            orient="records"
        )
    }