import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db_old as db_old

st.title("📈 Trend Analysis")

companies = db_old.get_companies()
pl = db_old.get_pl()

company = st.selectbox(
    "Select Company",
    companies["company_name"].sort_values()
)

ticker = companies.loc[
    companies["company_name"] == company,
    "id"
].iloc[0]

company_pl = pl[
    pl["company_id"] == ticker
].sort_values("year")

if len(company_pl):

    numeric = company_pl.select_dtypes(include="number").columns.tolist()

    metric = st.selectbox(
        "Select Metric",
        numeric
    )

    fig = px.line(
        company_pl,
        x="year",
        y=metric,
        markers=True,
        title=f"{metric} Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(company_pl)
else:
    st.warning("No Data Found")