import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("🤝 Peer Comparison")

peers = db.get_peers()

# Peer Group Dropdown
peer_groups = sorted(peers["peer_group"].dropna().unique())

selected_group = st.selectbox(
    "Select Peer Group",
    peer_groups
)

# Filter Data
result = peers[
    peers["peer_group"] == selected_group
]

st.success(f"{len(result)} Companies in {selected_group}")

# Show Table
st.dataframe(
    result,
    use_container_width=True,
    hide_index=True
)

# Benchmark Company
st.subheader("⭐ Benchmark Company")

benchmark = result[result["benchmark"] == "T"]

if benchmark.empty:
    benchmark = result[result["benchmark"] == 1]

if not benchmark.empty:
    st.success(f"Benchmark Company: {benchmark.iloc[0]['company_id']}")
else:
    st.info("No benchmark company found.")