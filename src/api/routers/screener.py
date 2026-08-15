import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from fastapi import APIRouter, HTTPException, Query

router = APIRouter(
    prefix="/screener",
    tags=["Screener"]
)

BASE_DIR = Path(__file__).resolve().parents[3]
DB = BASE_DIR / "db" / "nifty100.db"


def get_connection():
    """Create SQLite database connection."""
    return sqlite3.connect(DB)


def clean_columns(df):
    """Clean column names."""
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def load_table(table_name):
    """Load a SQLite table."""

    conn = get_connection()

    try:
        df = pd.read_sql(
            f'SELECT * FROM "{table_name}"',
            conn
        )
    finally:
        conn.close()

    return clean_columns(df)


def get_latest_records(df):
    """Get latest available record for each company."""

    if df.empty or "company_id" not in df.columns:
        return df

    df = df.copy()

    if "year" in df.columns:
        df["_year_num"] = (
            df["year"]
            .astype(str)
            .str.extract(r"(\d{4})")[0]
        )

        df["_year_num"] = pd.to_numeric(
            df["_year_num"],
            errors="coerce"
        )

        df = df.sort_values("_year_num")

    return df.groupby(
        "company_id",
        as_index=False
    ).tail(1)


@router.get("")
def get_screener(
    min_roe: float | None = Query(None),
    max_de: float | None = Query(None),
    sector: str | None = Query(None)
):
    """Screen companies using financial filters."""

    # ---------------------------
    # Validate parameters
    # ---------------------------

    if min_roe is not None and min_roe < 0:
        raise HTTPException(
            status_code=400,
            detail="min_roe cannot be negative"
        )

    if max_de is not None and max_de < 0:
        raise HTTPException(
            status_code=400,
            detail="max_de cannot be negative"
        )

    # ---------------------------
    # Load data
    # ---------------------------

    companies = load_table("companies")

    # IMPORTANT:
    # Your actual SQLite table name is financial_ratios
    ratios = load_table("financial_ratios")

    # ---------------------------
    # Standardize company ID
    # ---------------------------

    if "id" in companies.columns and "company_id" not in companies.columns:
        companies["company_id"] = companies["id"]

    companies["company_id"] = (
        companies["company_id"]
        .astype(str)
        .str.strip()
    )

    ratios["company_id"] = (
        ratios["company_id"]
        .astype(str)
        .str.strip()
    )

    # ---------------------------
    # Get latest financial data
    # ---------------------------

    ratios = get_latest_records(ratios)

    # ---------------------------
    # Merge companies and ratios
    # ---------------------------

    data = companies.merge(
        ratios,
        on="company_id",
        how="left",
        suffixes=("", "_ratio")
    )

    # ---------------------------
    # Convert numeric columns
    # ---------------------------

    for col in [
        "roe",
        "roce",
        "debt_to_equity"
    ]:
        if col in data.columns:
            data[col] = pd.to_numeric(
                data[col],
                errors="coerce"
            )

    # ---------------------------
    # Apply ROE filter
    # ---------------------------

    if min_roe is not None and "roe" in data.columns:
        data = data[
            data["roe"] >= min_roe
        ]

    # ---------------------------
    # Apply Debt/Equity filter
    # ---------------------------

    if max_de is not None and "debt_to_equity" in data.columns:
        data = data[
            data["debt_to_equity"] <= max_de
        ]

    # ---------------------------
    # Apply Sector filter
    # ---------------------------

    if sector is not None:

        sector_column = None

        for col in [
            "broad_sector",
            "sector",
            "sub_sector"
        ]:
            if col in data.columns:
                sector_column = col
                break

        if sector_column is not None:
            data = data[
                data[sector_column]
                .astype(str)
                .str.strip()
                .str.lower()
                == sector.strip().lower()
            ]

    # ---------------------------
    # Sort by ROE
    # ---------------------------

    if "roe" in data.columns:
        data = data.sort_values(
            "roe",
            ascending=False,
            na_position="last"
        )

    # ---------------------------
    # Select useful columns
    # ---------------------------

    columns_to_show = []

    for col in [
        "company_id",
        "id",
        "ticker",
        "company_name",
        "broad_sector",
        "sector",
        "roe",
        "roce",
        "debt_to_equity"
    ]:
        if col in data.columns:
            columns_to_show.append(col)

    if columns_to_show:
        data = data[columns_to_show]

    # ---------------------------
    # Make data JSON safe
    # ---------------------------

    data = data.replace(
        [np.inf, -np.inf],
        np.nan
    )

    data = data.astype(object)
    data = data.where(
        pd.notna(data),
        None
    )

    # ---------------------------
    # Return result
    # ---------------------------

    return {
        "count": int(len(data)),
        "filters": {
            "min_roe": min_roe,
            "max_de": max_de,
            "sector": sector
        },
        "companies": data.to_dict(
            orient="records"
        )
    }