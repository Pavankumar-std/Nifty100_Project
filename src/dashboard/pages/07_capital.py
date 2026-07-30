import streamlit as st
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("💰 Capital Allocation")

bs = db.get_bs()

st.metric("Records", len(bs))

numeric = bs.select_dtypes(include="number")

st.dataframe(bs.head(), use_container_width=True)

if len(numeric.columns) > 0:
    fig = px.box(
        numeric,
        title="Balance Sheet Metrics"
    )

    st.plotly_chart(fig, use_container_width=True)