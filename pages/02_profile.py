import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("🏢 Company Profile")

companies = db.get_companies()
ratios = db.get_ratios()
pros = db.get_pros()

company = st.selectbox(
    "Select Company",
    companies["company_name"].sort_values().unique()
)

company_row = companies[
    companies["company_name"] == company
].iloc[0]

ticker = company_row["id"]

st.success(f"Ticker : {ticker}")

st.subheader("Company Details")

col1, col2 = st.columns(2)

with col1:
    st.write("**Company** :", company_row["company_name"])
    st.write("**Website** :", company_row.get("website", "N/A"))

with col2:
    st.write("**Face Value** :", company_row.get("face_value", "N/A"))
    st.write("**Book Value** :", company_row.get("book_value", "N/A"))

company_ratio = ratios[
    ratios["company_id"] == ticker
].sort_values("year")

if len(company_ratio) > 0:

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "ROE",
        round(company_ratio.iloc[-1]["roe"], 2)
    )

    c2.metric(
        "ROCE",
        round(company_ratio.iloc[-1]["roce"], 2)
    )

    c3.metric(
        "Debt/Equity",
        round(company_ratio.iloc[-1]["debt_to_equity"], 2)
    )

    fig = px.line(
        company_ratio,
        x="year",
        y=["roe", "roce"],
        markers=True,
        title="ROE vs ROCE"
    )

    st.plotly_chart(fig, use_container_width=True)

st.subheader("Pros & Cons")

try:
    company_pros = pros[
        pros["company_id"] == ticker
    ]

    st.dataframe(
        company_pros,
        use_container_width=True
    )

except:
    st.info("Pros & Cons data not available.")