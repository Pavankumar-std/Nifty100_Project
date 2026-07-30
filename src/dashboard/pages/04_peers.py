import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("👥 Peer Comparison")

peer = db.get_peers()
companies = db.get_companies()

groups = sorted(peer["peer_group"].unique())

selected_group = st.selectbox(
    "Select Peer Group",
    groups
)

peer_df = peer[
    peer["peer_group"] == selected_group
]

st.metric("Companies", len(peer_df))

table = peer_df.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

st.dataframe(
    table[
        [
            "company_name",
            "company_id",
            "benchmark"
        ]
    ],
    use_container_width=True
)

fig = px.bar(
    table,
    x="company_name",
    y="benchmark",
    title=f"{selected_group} Companies"
)

st.plotly_chart(
    fig,
    use_container_width=True
)