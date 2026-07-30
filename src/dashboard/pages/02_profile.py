import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("🏢 Company Profile")

companies = db.get_companies()
ratios = db.get_ratios()
pl = db.get_pl()
pros = db.get_pros()
# --------------------
# Company Selector
# --------------------
company = st.selectbox(
    "Select Company",
    sorted(companies["company_name"].unique())
)

company_info = companies[
    companies["company_name"] == company
].iloc[0]

ticker = company_info["id"]

st.success(f"Ticker : {ticker}")

# --------------------
# Company Card
# --------------------
st.subheader(company)

st.write(company_info["about_company"])

# --------------------
# KPIs
# --------------------
ratio = ratios[
    ratios["company_id"] == ticker
].sort_values("year").iloc[-1]

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("ROE", round(ratio["roe"], 2))
c2.metric("ROCE", round(ratio["roce"], 2))
c3.metric("Debt/Equity", round(ratio["debt_to_equity"], 2))
c4.metric("ROA", round(ratio["roa"], 2))
c5.metric("Net Profit Margin", round(ratio["net_profit_margin"], 2))
# --------------------
# Revenue Chart
# --------------------
company_pl = pl[
    pl["company_id"] == ticker
].sort_values("year")

fig = px.bar(
    company_pl,
    x="year",
    y="sales",
    title="Revenue Trend"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("ROE vs ROCE Trend")

fig2 = px.line(
    company_pl.merge(
        ratios,
        on=["company_id", "year"]
    ),
    x="year",
    y=["roe", "roce"],
    markers=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.subheader("✅ Pros & Cons")

try:
    company_pros = pros[pros["company_id"] == ticker]

    if len(company_pros) > 0:
        st.success("Pros")

        for i in company_pros.columns:
            if "pro" in i.lower():
                value = company_pros.iloc[0][i]
                if pd.notna(value):
                    st.write("✅", value)

        st.error("Cons")

        for i in company_pros.columns:
            if "con" in i.lower():
                value = company_pros.iloc[0][i]
                if pd.notna(value):
                    st.write("❌", value)

except:
    st.info("No Pros & Cons available.")