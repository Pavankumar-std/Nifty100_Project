import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

# -------------------------------
# PAGE TITLE
# -------------------------------
st.title("🏠 Home Dashboard")

# -------------------------------
# LOAD DATA
# -------------------------------
companies = db.get_companies()
ratios = db.get_ratios()
sectors = db.get_sectors()

# Rename sector columns (your database imported headers incorrectly)
sectors.columns = [
    "company_id",
    "company_name",
    "sector",
    "sub_sector",
    "weight",
    "market_cap"
]

# -------------------------------
# KPI CALCULATIONS
# -------------------------------
avg_roe = round(ratios["roe"].mean(), 2)
avg_roce = round(ratios["roce"].mean(), 2)
median_de = round(ratios["debt_to_equity"].median(), 2)
debt_free = (ratios["debt_to_equity"] == 0).sum()

# -------------------------------
# KPI CARDS
# -------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("Average ROE", avg_roe)
c2.metric("Average ROCE", avg_roce)
c3.metric("Median D/E", median_de)
c4.metric("Debt Free Companies", debt_free)

st.divider()

# -------------------------------
# SECTOR DISTRIBUTION
# -------------------------------
st.subheader("📊 Sector Distribution")

sector_count = (
    sectors["sector"]
    .value_counts()
    .reset_index()
)

sector_count.columns = ["Sector", "Companies"]

fig = px.pie(
    sector_count,
    names="Sector",
    values="Companies",
    hole=0.45,
    title="Companies by Sector"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# -------------------------------
# TOP COMPANIES
# -------------------------------
st.subheader("🏆 Top Companies")

st.dataframe(
    companies[["company_name"]].head(10),
    use_container_width=True
)

st.divider()

# -------------------------------
# FINANCIAL RATIOS
# -------------------------------
st.subheader("📈 Financial Ratios")

st.dataframe(
    ratios.head(10),
    use_container_width=True
)