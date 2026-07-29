import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("🏭 Sector Analysis")

sectors = db.get_sectors()

sector_col = sectors.columns[1]

counts = sectors[sector_col].value_counts().reset_index()

counts.columns = ["Sector", "Companies"]

fig = px.bar(
    counts,
    x="Sector",
    y="Companies",
    title="Companies by Sector"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(sectors)