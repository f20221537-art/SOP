import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Microwave Biosensor: Dielectric Contrast Simulation")

# UI Sidebar for parameters
st.sidebar.header("Simulation Parameters")
tumor_size = st.sidebar.slider("Tumor Size (cells)", 10, 50, 20)
tumor_depth = st.sidebar.slider("Tumor Depth (index)", 50, 150, 100)
permittivity = st.sidebar.slider("Tumor Permittivity", 20.0, 60.0, 50.0)

# FDTD 1D Setup
size = 200
ez = np.zeros(size)
hx = np.zeros(size)
# Material array
epsilon = np.ones(size) * 5  # Background (Fat)
epsilon[tumor_depth : tumor_depth + tumor_size] = permittivity

# Simulation Loop
steps = 300
fig, ax = plt.subplots()

# Placeholder for animation
plot_area = st.empty()

for t in range(steps):
    # Update H-field
    hx[0:-1] = hx[0:-1] + 0.5 * (ez[1:] - ez[0:-1])
    
    # Update E-field
    ez[1:-1] = ez[1:-1] + (0.5 / epsilon[1:-1]) * (hx[1:-1] - hx[0:-2])
    
    # Add Gaussian source
    ez[50] = np.exp(-0.5 * ((t - 30) / 10)**2)
    
    # Visualization (update every 5 steps for speed)
    if t % 5 == 0:
        ax.clear()
        ax.plot(ez, label="Electric Field")
        ax.set_ylim(-1.5, 1.5)
        ax.set_title(f"Time Step: {t}")
        plot_area.pyplot(fig)

st.success("Simulation Complete")
