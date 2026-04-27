import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.header("1D FDTD Microwave Simulation")

# Sidebar Controls
with st.sidebar:
    st.subheader("Biological Parameters")
    # Expanded Tissue Library
    tissue_type = st.selectbox("Background Tissue", ["Fat", "Fibroglandular", "Skin", "Muscle"])
    tumor_depth = st.slider("Tumor Depth (mm)", 10, 100, 50, step=5)
    tumor_radius = st.slider("Tumor Radius (mm)", 5, 20, 10)
    
    st.subheader("Wave Parameters")
    freq = st.slider("Frequency (GHz)", 1.0, 10.0, 2.4, step=0.1)
    pulse_width = st.slider("Pulse Width (ns)", 0.1, 2.0, 0.5)
    sim_time = st.slider("Simulation Time (steps)", 100, 500, 300, step=50)

# Expanded Dielectric Constants (Approximate at microwave frequencies)
eps_r_map = {
    "Fat": 5.3, 
    "Fibroglandular": 15.0, 
    "Skin": 37.0, 
    "Muscle": 50.0, 
    "Tumor": 55.0
}

c0 = 3e8
dx = 0.001  # 1mm spatial step
size = 200  # grid size
dt = dx / (2 * c0)  # CFL condition

# Simulation Engine
def run_fdtd():
    ez = np.zeros(size)
    hy = np.zeros(size)
    
    # Material Profile Setup
    eps = np.ones(size) * eps_r_map[tissue_type]
    
    # Map mm to grid indices
    t_start = int(tumor_depth)
    t_end = t_start + int(tumor_radius * 2)
    
    # Ensure tumor stays within grid bounds
    if t_end < size:
        eps[t_start:t_end] = eps_r_map["Tumor"]
    
    frames = []
    # Gaussian pulse spread parameter based on user input
    spread = (pulse_width * 1e-9 / dt) ** 2 
    
    for t in range(sim_time):
        # Source (Gaussian Pulse modulated by continuous wave)
        ez[5] += np.exp(-((t - 50)**2) / spread) * np.sin(2 * np.pi * freq * 1e9 * t * dt)
        
        # Update H and E
        hy[:-1] += 0.5 * (ez[1:] - ez[:-1])
        ez[1:] += (0.5 / eps[1:]) * (hy[1:] - hy[:-1])
        
        # Capture frames for animation to reduce rendering load
        if t % 5 == 0:
            frames.append(go.Frame(data=[go.Scatter(x=np.arange(size), y=ez.copy())]))
            
    return frames, eps

frames, eps_profile = run_fdtd()

# Layout for the graph
fig = go.Figure(
    data=[go.Scatter(x=np.arange(size), y=np.zeros(size), name="E-Field")],
    layout=go.Layout(
        xaxis=dict(title="Depth (mm)"),
        yaxis=dict(range=[-2.0, 2.0], title="Electric Field Amplitude"),
        title=f"Wave Propagation through {tissue_type} with Tumor",
        updatemenus=[dict(type="buttons", buttons=[dict(label="Play Animation", method="animate", args=[None, {"frame": {"duration": 20, "redraw": True}, "fromcurrent": True}])])]
    ),
    frames=frames
)

fig.update_layout(template="plotly_dark", colorway=['#fde725']) # Viridis yellow for high contrast
st.plotly_chart(fig, use_container_width=True)

# Visualize the dielectric profile
st.subheader("Dielectric Profile ($\epsilon_r$)")
fig_eps = go.Figure(data=[go.Scatter(x=np.arange(size), y=eps_profile, fill='tozeroy', line_color='#440154')])
fig_eps.update_layout(template="plotly_dark", xaxis_title="Depth (mm)", yaxis_title="Relative Permittivity")
st.plotly_chart(fig_eps, use_container_width=True)
