import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("src"))

import dashboard.utils.db as db

st.title("💰 Capital Allocation")

bs = db.get_bs()
cf = db.get_cf()

c1, c2 = st.columns(2)

with c1:
    st.subheader("Balance Sheet")
    st.dataframe(bs.head(10), use_container_width=True)

with c2:
    st.subheader("Cash Flow")
    st.dataframe(cf.head(10), use_container_width=True)