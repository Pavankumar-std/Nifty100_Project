import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/sectors",
    tags=["Sectors"]
)

BASE_DIR = Path(__file__).resolve().parents[3]
DB_PATH = BASE_DIR / "db" / "nifty100.db"


def get_connection():
    """Create SQLite database connection."""
    return sqlite3.connect(str(DB_PATH))


def load_sectors():
    """Load sectors data with corrected column names."""

    conn = get_connection()

    try:
        df = pd.read_sql(
            'SELECT * FROM "sectors"',
            conn
        )
    finally:
        conn.close()

    # The original table headers are incorrect.
    # Rename columns according to the actual data.
    if len(df.columns) == 6:
        df.columns = [
            "company_id",
            "ticker",
            "broad_sector",
            "sub_sector",
            "value",
            "market_cap_category"
        ]

    return df


@router.get("")
def get_sectors():
    """Return sector summary."""

    df = load_sectors()

    result = (
        df.groupby("broad_sector")
        .agg(
            company_count=("company_id", "nunique")
        )
        .reset_index()
        .rename(
            columns={
                "broad_sector": "sector"
            }
        )
        .sort_values("sector")
    )

    return {
        "sectors": result.to_dict(
            orient="records"
        )
    }


@router.get("/{sector}/companies")
def get_sector_companies(sector: str):
    """Return companies in a sector."""

    df = load_sectors()

    filtered = df[
        df["broad_sector"]
        .astype(str)
        .str.strip()
        .str.lower()
        == sector.strip().lower()
    ].copy()

    if filtered.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Sector '{sector}' not found"
        )

    return {
        "sector": sector,
        "companies": filtered.to_dict(
            orient="records"
        )
    }