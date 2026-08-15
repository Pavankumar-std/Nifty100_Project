import sqlite3
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/companies",
    tags=["Documents"]
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


@router.get("/{ticker}/documents")
def get_company_documents(ticker: str):
    """Return available documents for a company."""

    conn = get_connection()

    try:
        companies = pd.read_sql(
            'SELECT * FROM "companies"',
            conn
        )

        documents = pd.read_sql(
            'SELECT * FROM "documents"',
            conn
        )

    finally:
        conn.close()

    companies = clean_columns(companies)
    documents = clean_columns(documents)

    # Ensure company_id exists
    if "id" in companies.columns and "company_id" not in companies.columns:
        companies["company_id"] = companies["id"]

    companies["company_id"] = companies["company_id"].astype(str)

    if "company_id" not in documents.columns:
        raise HTTPException(
            status_code=500,
            detail="company_id column not found in documents table"
        )

    documents["company_id"] = documents["company_id"].astype(str)

    # Find ticker
    ticker_column = None

    for col in ["ticker", "symbol"]:
        if col in companies.columns:
            ticker_column = col
            break

    if ticker_column is None:
        raise HTTPException(
            status_code=500,
            detail="Ticker column not found in companies table"
        )

    company = companies[
        companies[ticker_column]
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

    result = documents[
        documents["company_id"] == company_id
    ].copy()

    # Check possible URL columns
    url_columns = [
        col for col in result.columns
        if "url" in col or "link" in col
    ]

    if url_columns:

        for col in url_columns:
            result[f"{col}_is_url_valid"] = (
                result[col]
                .astype(str)
                .str.startswith(("http://", "https://"))
            )

    result = result.where(
        pd.notnull(result),
        None
    )

    return {
        "ticker": ticker,
        "company_id": company_id,
        "document_count": len(result),
        "documents": result.to_dict(
            orient="records"
        )
    }