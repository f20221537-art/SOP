import streamlit as st

st.header("Theoretical Background")

st.markdown("""
### Microwave-Tissue Interaction
The core principle of microwave cancer detection lies in the contrast of **dielectric properties**. 
Tumors typically contain higher water content than healthy fatty tissue, leading to significant differences in permittivity ($\epsilon_r$) and conductivity ($\sigma$).

#### Maxwell's Equations in Tissue
The propagation of the electric field ($\mathbf{E}$) and magnetic field ($\mathbf{H}$) is governed by:
""")

# Displaying Maxwell's Equations
st.latex(r"\nabla \times \mathbf{H} = \epsilon \frac{\partial \mathbf{E}}{\partial t} + \sigma \mathbf{E}")
st.latex(r"\nabla \times \mathbf{E} = -\mu \frac{\partial \mathbf{H}}{\partial t}")

st.info("""
**Research Focus:** We utilize the **Finite-Difference Time-Domain (FDTD)** method to discretize these equations in both space and time. 
This allows us to model complex pulse propagation through heterogeneous biological tissues.
""")

---

# Adding Resource Links
st.subheader("Project Resources")
col1, col2 = st.columns(2)

with col1:
    st.link_button("📂 View Project Drive", "https://drive.google.com/drive/folders/1yWdy-mrNFk-JRbryc35utEPD0a8QQB48")

with col2:
    st.link_button("💻 View GitHub Repository", "https://github.com/f20221537-art/Dheeraj_SOP_Simulator")
