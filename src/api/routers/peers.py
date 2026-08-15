import sqlite3
import pandas as pd

from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/peers",
    tags=["Peers"]
)

DB = "db/nifty100.db"


def get_connection():
    return sqlite3.connect(DB)


def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


@router.get("/{group_name}")
def get_peer_group(group_name: str):
    """Return companies and percentile data for a peer group."""

    conn = get_connection()

    peers = pd.read_sql(
        'SELECT * FROM "peer groups"',
        conn
    )

    companies = pd.read_sql(
        'SELECT * FROM "companies"',
        conn
    )

    try:
        percentiles = pd.read_sql(
            'SELECT * FROM "peer percentiles"',
            conn
        )
    except Exception:
        percentiles = pd.DataFrame()

    conn.close()

    peers = clean_columns(peers)
    companies = clean_columns(companies)

    if not percentiles.empty:
        percentiles = clean_columns(percentiles)

    # Find peer group column
    group_col = None

    for col in peers.columns:
        if "peer" in col and "group" in col:
            group_col = col
            break

    if group_col is None:
        raise HTTPException(
            status_code=500,
            detail="Peer group column not found"
        )

    filtered = peers[
        peers[group_col]
        .astype(str)
        .str.lower()
        == group_name.lower()
    ]

    if filtered.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Peer group '{group_name}' not found"
        )

    result = filtered.merge(
        companies,
        on="company_id",
        how="left"
    )

    # Add percentile information if available
    if not percentiles.empty and "company_id" in percentiles.columns:

        percentile_group_col = None

        for col in percentiles.columns:
            if "peer" in col and "group" in col:
                percentile_group_col = col
                break

        if percentile_group_col:

            percentile_data = percentiles[
                percentiles[percentile_group_col]
                .astype(str)
                .str.lower()
                == group_name.lower()
            ]

            result = result.merge(
                percentile_data,
                on="company_id",
                how="left",
                suffixes=("", "_percentile")
            )

    result = result.where(
        pd.notnull(result),
        None
    )

    return {
        "peer_group": group_name,
        "company_count": len(result),
        "companies": result.to_dict(
            orient="records"
        )
    }