import streamlit as st
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

bs = db.get_bs()

st.title("💰 Capital Allocation")

numeric = bs.select_dtypes(include="number").columns

if len(numeric) >= 2:

    fig = px.scatter(
        bs,
        x=numeric[0],
        y=numeric[1],
        title="Capital Allocation"
    )

    st.plotly_chart(fig, use_container_width=True)

st.dataframe(bs)