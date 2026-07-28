import sqlite3
import pandas as pd
import streamlit as st

DB = "db/nifty100.db"


@st.cache_data
def load_table(table):
    conn = sqlite3.connect(DB)
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df


def get_companies():
    return load_table("companies")


def get_ratios():
    return load_table("financial_ratios")


def get_sectors():
    return load_table("sectors")


def get_pros():
    return load_table("prosandcons")


def get_pl():
    return load_table("profitandloss")


def get_bs():
    return load_table("balancesheet")


def get_cf():
    return load_table("cashflow")


def get_peers():
    return load_table("peer_groups")