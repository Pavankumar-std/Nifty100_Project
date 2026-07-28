import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("📄 Reports")

companies = db.get_companies()

st.subheader("Companies")

st.dataframe(
    companies[["company_name"]],
    use_container_width=True,
    hide_index=True
)

csv = companies.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Company Report",
    csv,
    "companies_report.csv",
    "text/csv"
)