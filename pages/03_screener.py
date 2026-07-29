import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("📊 Stock Screener")

ratios = db.get_ratios()
companies = db.get_companies()

# --------------------
# Sidebar Filters
# --------------------
st.sidebar.header("Filter Companies")

roe = st.sidebar.slider("Minimum ROE", 0, 100, 15)
roce = st.sidebar.slider("Minimum ROCE", 0, 100, 15)
de = st.sidebar.slider("Maximum Debt/Equity", 0.0, 5.0, 1.0)
icr = st.sidebar.slider("Minimum Interest Coverage", 0.0, 20.0, 2.0)

filtered = ratios[
    (ratios["roe"] >= roe) &
    (ratios["roce"] >= roce) &
    (ratios["debt_to_equity"] <= de) &
    (ratios["interest_coverage"] >= icr)
]

result = filtered.merge(
    companies,
    left_on="company_id",
    right_on="id"
)

st.success(f"{len(result)} Companies Found")

st.dataframe(
    result[
        [
            "company_name",
            "company_id",
            "roe",
            "roce",
            "debt_to_equity",
            "interest_coverage"
        ]
    ],
    use_container_width=True
)

csv = result.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download CSV",
    csv,
    "screener_output.csv",
    "text/csv"
)