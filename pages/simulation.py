import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.header("1D FDTD: Healthy vs. Tumor Comparison")

# Sidebar Controls
with st.sidebar:
    st.subheader("Biological Parameters")
    tissue_type = st.selectbox("Background Tissue", ["Fat", "Fibroglandular", "Skin", "Muscle"])
    tumor_depth = st.slider("Tumor Depth (mm)", 10, 100, 50)
    tumor_radius = st.slider("Tumor Radius (mm)", 5, 20, 10)
    
    st.subheader("Wave Parameters")
    freq = st.slider("Frequency (GHz)", 1.0, 10.0, 2.4)
    pulse_width = st.slider("Pulse Width (ns)", 0.1, 2.0, 0.5)
    
    # EXTENDED TIME: Range increased to 2000 steps
    sim_time = st.slider("Simulation Time (steps)", 100, 2000, 1200, step=100)

# Constants & Setup
eps_r_map = {"Fat": 5.3, "Fibroglandular": 15.0, "Skin": 37.0, "Muscle": 50.0, "Tumor": 55.0}
c0 = 3e8
dx = 0.001 
size = 200 
dt = dx / (2 * c0) 

@st.cache_data
def run_dual_fdtd(tissue, t_depth, t_radius, frequency, p_width, s_time):
    ez_h, hy_h = np.zeros(size), np.zeros(size)
    ez_t, hy_t = np.zeros(size), np.zeros(size)
    
    eps_h = np.ones(size) * eps_r_map[tissue]
    eps_t = np.ones(size) * eps_r_map[tissue]
    
    t_start, t_end = int(t_depth), int(t_depth + t_radius * 2)
    if t_end < size:
        eps_t[t_start:t_end] = eps_r_map["Tumor"]
        
    frames = []
    spread = (p_width * 1e-9 / dt) ** 2 
    
    for t in range(s_time):
        source_val = np.exp(-((t - 50)**2) / spread) * np.sin(2 * np.pi * frequency * 1e9 * t * dt)
        ez_h[5] += source_val
        ez_t[5] += source_val
        
        # Standard Update Equations
        hy_h[:-1] += 0.5 * (ez_h[1:] - ez_h[:-1])
        ez_h[1:] += (0.5 / eps_h[1:]) * (hy_h[1:] - hy_h[:-1])
        
        hy_t[:-1] += 0.5 * (ez_t[1:] - ez_t[:-1])
        ez_t[1:] += (0.5 / eps_t[1:]) * (hy_t[1:] - hy_t[:-1])
        
        # Frame capture (sampled at t%10 to maintain performance at 2000 steps)
        if t % 10 == 0:
            frames.append(go.Frame(
                data=[go.Scatter(y=ez_h.copy()), go.Scatter(y=ez_t.copy())],
                traces=[0, 1]
            ))
            
    return frames, eps_h, eps_t

# Run Simulation
frames, eps_healthy, eps_tumor = run_dual_fdtd(tissue_type, tumor_depth, tumor_radius, freq, pulse_width, sim_time)

# Visualization with Subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=("Healthy Tissue", "Tumor Tissue"))

# Traces with original Axis Name convention
fig.add_trace(go.Scatter(x=np.arange(size), y=np.zeros(size), name="Healthy", line=dict(color="#00b4d8")), row=1, col=1)
fig.add_trace(go.Scatter(x=np.arange(size), y=np.zeros(size), name="Tumor", line=dict(color="#fde725")), row=1, col=2)

fig.update_layout(
    template="plotly_dark",
    yaxis=dict(range=[-2.0, 2.0], title="Amplitude"),
    yaxis2=dict(range=[-2.0, 2.0]),
    xaxis=dict(title="Grid Position (mm)"), # Maintained name
    xaxis2=dict(title="Grid Position (mm)"), # Maintained name
    updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None, {"frame": {"duration": 10, "redraw": False}}])])]
)

fig.frames = frames
st.plotly_chart(fig, use_container_width=True)
