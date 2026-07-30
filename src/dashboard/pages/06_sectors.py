import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("🏭 Sector Analysis")

sectors = db.get_sectors()

sector_col = sectors.columns[2]

selected = st.selectbox(
    "Select Sector",
    sorted(sectors[sector_col].unique())
)

filtered = sectors[
    sectors[sector_col] == selected
]

st.metric("Companies", len(filtered))

st.dataframe(filtered, use_container_width=True)

fig = px.histogram(
    filtered,
    x=sector_col,
    title="Sector Distribution"
)

st.plotly_chart(fig, use_container_width=True)