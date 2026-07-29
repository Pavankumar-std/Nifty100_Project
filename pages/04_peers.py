import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("🤝 Peer Comparison")

companies = db.get_companies()
ratios = db.get_ratios()
peers = db.get_peers()

company = st.selectbox(
    "Select Company",
    companies["company_name"].sort_values()
)

ticker = companies.loc[
    companies["company_name"] == company,
    "id"
].iloc[0]

company_ratio = ratios[
    ratios["company_id"] == ticker
].sort_values("year")

if len(company_ratio) > 0:

    latest = company_ratio.iloc[-1]

    chart = px.bar(
        x=["ROE","ROCE","Debt/Equity","Interest Coverage"],
        y=[
            latest["roe"],
            latest["roce"],
            latest["debt_to_equity"],
            latest["interest_coverage"]
        ],
        title="Company Financial Metrics"
    )

    st.plotly_chart(chart, use_container_width=True)

st.subheader("Peer Group")

st.dataframe(
    peers.head(20),
    use_container_width=True
)