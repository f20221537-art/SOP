import streamlit as st

st.set_page_config(page_title="Microwave Cancer Detection Lab", layout="wide")

# Define pages
theory_page = st.Page("pages/theory.py", title="Theoretical Background", icon="📖")
sim_1d_page = st.Page("pages/simulation.py", title="1D FDTD Simulation", icon="🌊")
sim_2d_page = st.Page("pages/phantom_2d.py", title="2D Phantom Modeler", icon="🎯")
analysis_page = st.Page("pages/analysis.py", title="Performance Analysis", icon="📊")

# Navigation logic
pg = st.navigation({
    "Research": [theory_page],
    "Simulations": [sim_1d_page, sim_2d_page],
    "Analytics": [analysis_page]
})

pg.run()
