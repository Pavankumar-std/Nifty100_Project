import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("📊 Stock Screener")

# -----------------------------
# Load Data
# -----------------------------
ratios = db.get_ratios()
companies = db.get_companies()

# -----------------------------
# Sidebar Presets
# -----------------------------
st.sidebar.header("📌 Preset Filters")

preset = st.sidebar.selectbox(
    "Choose Preset",
    [
        "Custom",
        "Quality",
        "Value",
        "Growth"
    ]
)

if preset == "Quality":
    roe = 15
    de = 1.0

elif preset == "Value":
    roe = 10
    de = 2.0

elif preset == "Growth":
    roe = 20
    de = 1.5

else:
    roe = st.sidebar.slider(
        "Minimum ROE",
        0,
        100,
        15
    )

    de = st.sidebar.slider(
        "Maximum Debt / Equity",
        0.0,
        5.0,
        1.0
    )

# -----------------------------
# Apply Filters
# -----------------------------
filtered = ratios[
    (ratios["roe"] >= roe) &
    (ratios["debt_to_equity"] <= de)
]

# -----------------------------
# Merge Company Details
# -----------------------------
result = filtered.merge(
    companies,
    left_on="company_id",
    right_on="id"
)

# -----------------------------
# Result Count
# -----------------------------
st.success(f"✅ {len(result)} Companies Match Your Filters")

# -----------------------------
# Results Table
# -----------------------------
st.dataframe(
    result[
        [
            "company_name",
            "company_id",
            "roe",
            "roce",
            "debt_to_equity"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Download CSV
# -----------------------------
csv = result.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Screener Results",
    data=csv,
    file_name="screener_output.csv",
    mime="text/csv"
)

# -----------------------------
# Filter Summary
# -----------------------------
st.divider()

st.subheader("📋 Current Filter Summary")

c1, c2 = st.columns(2)

c1.metric("Minimum ROE", roe)

c2.metric("Maximum D/E", de)