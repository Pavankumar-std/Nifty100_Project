import streamlit as st
import plotly.express as px
import sys
import os
import pandas as pd

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.set_page_config(
    page_title="Nifty100 Analytics",
    layout="wide"
)

st.title("🏠 Home Dashboard")

# -----------------------
# Load Data
# -----------------------
companies = db.get_companies()
ratios = db.get_ratios()

# Clean year column
ratios["year"] = ratios["year"].astype(str).str.strip()

# Convert numeric columns
numeric_cols = ["roe", "roce", "debt_to_equity"]

for col in numeric_cols:
    if col in ratios.columns:
        ratios[col] = pd.to_numeric(ratios[col], errors="coerce")

# -----------------------
# Sidebar
# -----------------------
years = sorted(ratios["year"].dropna().unique())

if "TTM" in years:
    years.remove("TTM")

default_year = "Mar 2024" if "Mar 2024" in years else years[-1]

year = st.sidebar.selectbox(
    "Select Year",
    years,
    index=years.index(default_year)
)

ratios = ratios[ratios["year"] == year]

# -----------------------
# KPIs
# -----------------------
avg_roe = round(ratios["roe"].mean(), 2)
avg_roce = round(ratios["roce"].mean(), 2)
median_de = round(ratios["debt_to_equity"].median(), 2)
total_companies = len(companies)
debt_free = (ratios["debt_to_equity"] == 0).sum()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Average ROE", avg_roe)
c2.metric("Average ROCE", avg_roce)
c3.metric("Median D/E", median_de)
c4.metric("Companies", total_companies)
c5.metric("Debt Free", debt_free)

st.divider()

# -----------------------
# Sector Distribution
# -----------------------
sector_df = db.get_sectors()

sector_counts = (
    sector_df.iloc[:, 2]
    .value_counts()
    .reset_index()
)

sector_counts.columns = ["Sector", "Count"]

fig = px.pie(
    sector_counts,
    names="Sector",
    values="Count",
    hole=0.5,
    title="Sector Distribution"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -----------------------
# Top 5 Companies by ROE
# -----------------------
st.subheader("🏆 Top 5 Companies by ROE")

top5 = (
    ratios.sort_values("roe", ascending=False)
    .head(5)
    .merge(
        companies,
        left_on="company_id",
        right_on="id"
    )
)

st.dataframe(
    top5[
        [
            "company_name",
            "roe",
            "roce",
            "debt_to_equity"
        ]
    ],
    use_container_width=True
)