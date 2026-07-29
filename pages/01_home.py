import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db
import plotly.express as px

st.title("🏠 Nifty100 Home Dashboard")

companies = db.get_companies()
ratios = db.get_ratios()
sectors = db.get_sectors()

# -----------------------------
# Sidebar
# -----------------------------
years = sorted(ratios["year"].unique())

selected_year = st.sidebar.selectbox(
    "Select Year",
    years,
    index=len(years)-1
)

ratios = ratios[ratios["year"] == selected_year]

# -----------------------------
# KPIs
# -----------------------------
avg_roe = round(ratios["roe"].mean(),2)
avg_roce = round(ratios["roce"].mean(),2)
median_de = round(ratios["debt_to_equity"].median(),2)
companies_count = len(companies)

c1,c2,c3,c4 = st.columns(4)

c1.metric("Average ROE",avg_roe)
c2.metric("Average ROCE",avg_roce)
c3.metric("Median D/E",median_de)
c4.metric("Companies",companies_count)

st.divider()

# -----------------------------
# Sector Distribution
# -----------------------------
st.subheader("Sector Distribution")

sector_col = sectors.columns[1]

sector_counts = (
    sectors[sector_col]
    .value_counts()
    .reset_index()
)

sector_counts.columns=["Sector","Companies"]

fig = px.pie(
    sector_counts,
    names="Sector",
    values="Companies",
    hole=0.5,
    title="Companies by Sector"
)

st.plotly_chart(fig,use_container_width=True)

# -----------------------------
# Top ROE Companies
# -----------------------------
st.subheader("Top 5 Companies by ROE")

top = (
    ratios.sort_values(
        "roe",
        ascending=False
    )
    .head(5)
)

top = top.merge(
    companies,
    left_on="company_id",
    right_on="id"
)

st.dataframe(
    top[
        [
            "company_name",
            "roe",
            "roce",
            "debt_to_equity"
        ]
    ],
    use_container_width=True
)