import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("📄 Annual Reports")

companies = db.get_companies()

company = st.selectbox(
    "Company",
    companies["company_name"]
)

selected = companies[
    companies["company_name"] == company
].iloc[0]

st.write("### Company Details")

st.write(selected)

csv = companies.to_csv(index=False).encode()

st.download_button(
    "Download Company List",
    csv,
    "companies.csv",
    "text/csv"
)