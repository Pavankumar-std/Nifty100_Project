import sqlite3
import pandas as pd
import streamlit as st

DB = "db/nifty100.db"


def clean_columns(df):
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df


@st.cache_data(ttl=600)
def load_table(table):
    conn = sqlite3.connect(DB)
    df = pd.read_sql(f'SELECT * FROM "{table}"', conn)
    conn.close()
    return clean_columns(df)


# -----------------------------
# Companies
# -----------------------------
def get_companies():
    return load_table("companies")


# -----------------------------
# Financial Ratios
# -----------------------------
def get_ratios(ticker=None, year=None):
    df = load_table("financial_ratios")

    if ticker is not None:
        df = df[df["company_id"] == ticker]

    if year is not None:
        df = df[df["year"] == year]

    return df


# -----------------------------
# Profit & Loss
# -----------------------------
def get_pl(ticker=None):
    df = load_table("profitandloss")

    if ticker is not None:
        df = df[df["company_id"] == ticker]

    return df


# -----------------------------
# Balance Sheet
# -----------------------------
def get_bs(ticker=None):
    df = load_table("balancesheet")

    if ticker is not None:
        df = df[df["company_id"] == ticker]

    return df


# -----------------------------
# Cash Flow
# -----------------------------
def get_cf(ticker=None):
    df = load_table("cashflow")

    if ticker is not None:
        df = df[df["company_id"] == ticker]

    return df


# -----------------------------
# Sectors
# -----------------------------
def get_sectors():
    return load_table("sectors")


# -----------------------------
# Peer Groups
# -----------------------------
def get_peers(group_name=None):
    df = load_table("peer_groups")

    if group_name is not None:
        df = df[df["peer_group"] == group_name]

    return df

    if group_name is not None:
        df = df[df["peer_group"] == group_name]

    return df


# -----------------------------
# Market Cap / Valuation
# -----------------------------
def get_valuation():
    try:
        return load_table("market cap")
    except:
        return pd.DataFrame()


# -----------------------------
# Pros & Cons
# -----------------------------
def get_pros():
    try:
        return load_table("prosandcons")
    except:
        return pd.DataFrame()