import streamlit as st

st.set_page_config(page_title="Microwave Cancer Detection Lab", layout="wide")

# Define pages
theory_page = st.Page("pages/theory.py", title="Theoretical Background", icon="📖")
sim_page = st.Page("pages/simulation.py", title="Wave Simulation (FDTD)", icon="🌊")
analysis_page = st.Page("pages/analysis.py", title="Performance Analysis", icon="📊")

# Navigation logic
pg = st.navigation({
    "Research": [theory_page],
    "Laboratory": [sim_page, analysis_page]
})

pg.run()
