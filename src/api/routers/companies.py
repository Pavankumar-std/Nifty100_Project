import sqlite3
import math
import pandas as pd

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse


router = APIRouter()


DB = "db/nifty100.db"


def get_connection():
    """Create SQLite database connection."""
    return sqlite3.connect(DB)


def clean_columns(df):
    """Clean dataframe column names."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


def clean_json(data):
    """Replace NaN and infinity values with None."""

    if isinstance(data, dict):
        return {
            key: clean_json(value)
            for key, value in data.items()
        }

    if isinstance(data, list):
        return [clean_json(item) for item in data]

    if isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return None

    return data


def load_table(table_name):
    """Load a database table."""

    conn = get_connection()

    df = pd.read_sql(
        f'SELECT * FROM "{table_name}"',
        conn
    )

    conn.close()

    return clean_columns(df)


@router.get("/companies")
def get_all_companies(
    sector: str | None = None,
    market_cap_category: str | None = None,
    search: str | None = None
):
    """Return all companies with optional filters."""

    companies = load_table("companies")

    # Optional sector filter
    if sector and "broad_sector" in companies.columns:
        companies = companies[
            companies["broad_sector"]
            .astype(str)
            .str.lower()
            == sector.lower()
        ]

    # Optional market cap category filter
    if market_cap_category and "market_cap_category" in companies.columns:
        companies = companies[
            companies["market_cap_category"]
            .astype(str)
            .str.lower()
            == market_cap_category.lower()
        ]

    # Optional search filter
    if search:

        search_lower = search.lower()

        name_match = pd.Series(
            False,
            index=companies.index
        )

        id_match = pd.Series(
            False,
            index=companies.index
        )

        if "company_name" in companies.columns:
            name_match = (
                companies["company_name"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_lower,
                    na=False
                )
            )

        if "id" in companies.columns:
            id_match = (
                companies["id"]
                .astype(str)
                .str.lower()
                .str.contains(
                    search_lower,
                    na=False
                )
            )

        companies = companies[name_match | id_match]

    # Convert dataframe to records
    records = companies.to_dict(
        orient="records"
    )

    # IMPORTANT: Remove NaN and infinity
    records = clean_json(records)

    return records


@router.get("/companies/{ticker}")
def get_company(ticker: str):
    """Return a single company profile."""

    companies = load_table("companies")

    result = pd.DataFrame()

    # Search by id
    if "id" in companies.columns:
        result = companies[
            companies["id"]
            .astype(str)
            .str.upper()
            == ticker.upper()
        ]

    # Search by company_id if needed
    if result.empty and "company_id" in companies.columns:
        result = companies[
            companies["company_id"]
            .astype(str)
            .str.upper()
            == ticker.upper()
        ]

    if result.empty:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    record = result.iloc[0].to_dict()

    return clean_json(record)


@router.get("/companies/{ticker}/pl")
def get_company_pl(
    ticker: str,
    from_year: str | None = None,
    to_year: str | None = None
):
    """Return company profit and loss history."""

    df = load_table("profitandloss")

    df = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if from_year:
        df = df[df["year"].astype(str) >= from_year]

    if to_year:
        df = df[df["year"].astype(str) <= to_year]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Company data not found"
        )

    records = df.to_dict(orient="records")

    return clean_json(records)


@router.get("/companies/{ticker}/bs")
def get_company_bs(
    ticker: str,
    from_year: str | None = None,
    to_year: str | None = None
):
    """Return company balance sheet history."""

    df = load_table("balancesheet")

    df = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if from_year:
        df = df[df["year"].astype(str) >= from_year]

    if to_year:
        df = df[df["year"].astype(str) <= to_year]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Company data not found"
        )

    records = df.to_dict(orient="records")

    return clean_json(records)


@router.get("/companies/{ticker}/cashflow")
def get_company_cashflow(
    ticker: str,
    from_year: str | None = None,
    to_year: str | None = None
):
    """Return company cash flow history."""

    df = load_table("cashflow")

    df = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if from_year:
        df = df[df["year"].astype(str) >= from_year]

    if to_year:
        df = df[df["year"].astype(str) <= to_year]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Company data not found"
        )

    records = df.to_dict(orient="records")

    return clean_json(records)


@router.get("/companies/{ticker}/ratios")
def get_company_ratios(
    ticker: str,
    year: str | None = None
):
    """Return company financial ratios."""

    df = load_table("financial ratios")

    df = df[
        df["company_id"]
        .astype(str)
        .str.upper()
        == ticker.upper()
    ]

    if year:
        df = df[
            df["year"]
            .astype(str)
            == str(year)
        ]

    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Financial ratios not found"
        )

    records = df.to_dict(orient="records")

    return clean_json(records)


@router.get("/companies/{ticker}/tearsheet")
def get_company_tearsheet(ticker: str):
    """Download company tearsheet PDF."""

    file_path = (
        f"reports/tearsheets/{ticker}.pdf"
    )

    try:
        return FileResponse(
            file_path,
            media_type="application/pdf",
            filename=f"{ticker}_tearsheet.pdf"
        )

    except Exception:
        raise HTTPException(
            status_code=404,
            detail="Tearsheet not found"
        )