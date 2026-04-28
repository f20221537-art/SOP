import streamlit as st

st.header("Theoretical Background")

# --- Core Physics Section ---
st.markdown("""
### Microwave-Tissue Interaction
The core principle of microwave cancer detection lies in the contrast of dielectric properties. 
Tumors typically contain higher water content than healthy fatty tissue, leading to significant 
differences in permittivity ($\epsilon_r$) and conductivity ($\sigma$).
""")

# Maxwell's Equations
st.latex(r"\nabla \times \mathbf{H} = \epsilon \frac{\partial \mathbf{E}}{\partial t} + \sigma \mathbf{E}")
st.latex(r"\nabla \times \mathbf{E} = -\mu \frac{\partial \mathbf{H}}{\partial t}")

st.info("**Research Focus:** We utilize the Finite-Difference Time-Domain (FDTD) method to discretize these equations in both space and time.")

# --- Project Resources Section ---
st.divider()
st.subheader("🔗 Research & Source Code")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Documentation & Slides**")
    st.write("Access clinical data and academic presentations.")
    st.link_button("Open Google Drive", "https://drive.google.com/drive/folders/1yWdy-mrNFk-JRbryc35utEPD0a8QQB48")

with col2:
    st.markdown("**SOP Simulator Code**")
    st.write("View the full implementation and logic on GitHub.")
    st.link_button("View GitHub Repo", "https://github.com/f20221537-art/Dheeraj_SOP_Simulator")

st.caption("Developed for Undergraduate Research Project: Microwave Biosensors.")
