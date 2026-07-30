import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("📑 Reports")

companies = db.get_companies()

company = st.selectbox(
    "Company",
    sorted(companies["company_name"])
)

st.success("Annual Reports Module Ready")

st.info("Report links will be integrated in Sprint 5.")

st.dataframe(
    companies[["company_name"]].head(20),
    use_container_width=True
)