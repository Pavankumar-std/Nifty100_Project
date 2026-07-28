import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("🏭 Sector Analysis")

sectors = db.get_sectors()

st.subheader("Sector Dataset")

st.dataframe(
    sectors,
    use_container_width=True,
    hide_index=True
)

st.subheader("Companies by Sector")

sector_col = sectors.columns[1]

counts = sectors[sector_col].value_counts()

st.bar_chart(counts)