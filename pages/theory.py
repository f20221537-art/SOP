import streamlit as st

st.header("Theoretical Background")
st.markdown("""
### Microwave-Tissue Interaction
The core principle of microwave cancer detection lies in the contrast of dielectric properties. 
Tumors typically contain higher water content than healthy fatty tissue, leading to significant differences in permittivity ($\epsilon_r$) and conductivity ($\sigma$).

#### Maxwell's Equations in Tissue
The propagation of the electric field ($E$) is governed by:
""")

st.latex(r"\nabla \times \mathbf{H} = \epsilon \frac{\partial \mathbf{E}}{\partial t} + \sigma \mathbf{E}")
st.latex(r"\nabla \times \mathbf{E} = -\mu \frac{\partial \mathbf{H}}{\partial t}")

st.info("**Research Focus:** We utilize the Finite-Difference Time-Domain (FDTD) method to discretize these equations in both space and time.")
