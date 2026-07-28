import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db
import pandas as pd

st.title("📈 Trend Analysis")

companies = db.get_companies()
pl = db.get_pl()

company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

selected = companies[
    companies["company_name"] == company
]

ticker = selected.iloc[0]["id"]

st.write("Ticker:", ticker)

# Filter Profit/Loss data
trend = pl[
    pl["company_id"] == ticker
]

if len(trend) > 0:
    st.subheader("Financial Trend")

    st.line_chart(
        trend.select_dtypes(
            include="number"
        )
    )

    st.dataframe(
        trend,
        use_container_width=True
    )

else:
    st.warning("No trend data available")