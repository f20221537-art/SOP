import streamlit as st
import numpy as np
import plotly.express as px

st.header("2D Tissue Phantom Modeler")
st.markdown("""
Before running complex 2D or 3D FDTD simulations, researchers build **digital phantoms** to map the spatial distribution of dielectric properties. 
This tool generates a 2D permittivity ($\epsilon_r$) cross-section, highlighting the dielectric contrast necessary for microwave tomography.
""")

# Setup grid
grid_size = 150
x = np.linspace(-75, 75, grid_size)
y = np.linspace(-75, 75, grid_size)
X, Y = np.meshgrid(x, y)

# Sidebar Controls
with st.sidebar:
    st.subheader("Phantom Geometry")
    bg_tissue = st.selectbox("Bulk Tissue", ["Fat ($\epsilon_r=5.3$)", "Fibroglandular ($\epsilon_r=15$)"])
    
    st.subheader("Tumor Coordinates")
    t_x = st.slider("X Position (mm)", -40, 40, 15)
    t_y = st.slider("Y Position (mm)", -40, 40, -10)
    t_radius = st.slider("Radius (mm)", 5, 20, 12)
    
    st.subheader("Skin Layer")
    skin_thickness = st.slider("Thickness (mm)", 1, 5, 2)

# Map selections to values
eps_bg = 5.3 if "Fat" in bg_tissue else 15.0
eps_skin = 37.0
eps_tumor = 55.0

# Initialize Phantom Array
phantom = np.ones((grid_size, grid_size))

# Define geometry limits
outer_radius = 60
inner_radius = outer_radius - skin_thickness

# Build the phantom matrix
for i in range(grid_size):
    for j in range(grid_size):
        r_dist = np.sqrt(X[i, j]**2 + Y[i, j]**2)
        
        # Free space background
        if r_dist > outer_radius:
            phantom[i, j] = 1.0 
        # Skin Layer
        elif r_dist > inner_radius:
            phantom[i, j] = eps_skin
        # Bulk Tissue
        else:
            phantom[i, j] = eps_bg
            
        # Add Tumor
        t_dist = np.sqrt((X[i, j] - t_x)**2 + (Y[i, j] - t_y)**2)
        if t_dist <= t_radius and r_dist <= inner_radius:
            phantom[i, j] = eps_tumor

# Render Heatmap
fig = px.imshow(
    phantom, 
    x=x, y=y,
    color_continuous_scale="Viridis",
    labels=dict(color="Permittivity (εr)"),
    title="2D Dielectric Map"
)

fig.update_layout(
    template="plotly_dark",
    xaxis_title="X Axis (mm)",
    yaxis_title="Y Axis (mm)",
    coloraxis_colorbar=dict(title="$\epsilon_r$")
)

st.plotly_chart(fig, use_container_width=True)

# Analytics column below the graph
col1, col2 = st.columns(2)
with col1:
    st.info(f"**Max Permittivity Contrast:** {eps_tumor / eps_bg:.2f}:1")
with col2:
    st.info("**Scattering Cross-Section Target:** Distinct")
