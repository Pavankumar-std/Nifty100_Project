import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("🏢 Company Profile")

companies = db.get_companies()
ratios = db.get_ratios()

# Select Company
company = st.selectbox(
    "Select Company",
    companies["company_name"]
)

# Get selected company
selected = companies[
    companies["company_name"] == company
]

ticker = selected.iloc[0]["id"]

st.subheader(company)

st.write("Ticker:", ticker)

# Company Details
st.dataframe(
    selected,
    use_container_width=True
)

# Financial Ratios
company_ratio = ratios[
    ratios["company_id"] == ticker
]

st.subheader("Financial Ratios")

st.dataframe(
    company_ratio,
    use_container_width=True
)