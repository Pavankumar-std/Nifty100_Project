import streamlit as st

st.set_page_config(
    page_title="Nifty100 Financial Intelligence Platform",
    page_icon="📊",
    layout="wide"
)

home = st.Page("pages/01_home.py", title="🏠 Home")
profile = st.Page("pages/02_profile.py", title="🏢 Company Profile")
screener = st.Page("pages/03_screener.py", title="🔍 Screener")
peers = st.Page("pages/04_peers.py", title="👥 Peers")
trends = st.Page("pages/05_trends.py", title="📈 Trends")
sectors = st.Page("pages/06_sectors.py", title="🏭 Sectors")
capital = st.Page("pages/07_capital.py", title="💰 Capital")
reports = st.Page("pages/08_reports.py", title="📄 Reports")

pg = st.navigation(
    [
        home,
        profile,
        screener,
        peers,
        trends,
        sectors,
        capital,
        reports,
    ]
)

pg.run()