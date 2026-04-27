import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide") # Wider layout for better side-by-side viewing
st.header("1D FDTD: Healthy vs. Tumor Tissue")
st.markdown("Compare wave propagation side-by-side to observe backscatter and phase delays.")

# --- Sidebar Controls ---
with st.sidebar:
    st.subheader("Biological Parameters")
    tissue_type = st.selectbox("Background Tissue", ["Fat", "Fibroglandular", "Skin", "Muscle"])
    tumor_depth = st.slider("Tumor Depth (mm)", 10, 250, 80, step=5) # Increased range
    tumor_radius = st.slider("Tumor Radius (mm)", 5, 20, 10)
    
    st.subheader("Wave Parameters")
    freq = st.slider("Frequency (GHz)", 1.0, 10.0, 2.4, step=0.1)
    pulse_width = st.slider("Pulse Width (ns)", 0.1, 2.0, 0.5)
    # INCREASED: Simulation Time slider now goes up to 2000
    sim_time = st.slider("Simulation Time (steps)", 100, 2000, 1000, step=100)

# Expanded Dielectric Constants
eps_r_map = {
    "Fat": 5.3, 
    "Fibroglandular": 15.0, 
    "Skin": 37.0, 
    "Muscle": 50.0, 
    "Tumor": 55.0
}

c0 = 3e8
dx = 0.001  # 1mm spatial step
size = 400  # INCREASED: Grid size increased from 200 to 400 to prevent edge collision
dt = dx / (2 * c0)  # CFL condition

@st.cache_data
def run_dual_fdtd(tissue, t_depth, t_radius, frequency, p_width, s_time):
    ez_h = np.zeros(size)
    hy_h = np.zeros(size)
    eps_h = np.ones(size) * eps_r_map[tissue]
    
    ez_t = np.zeros(size)
    hy_t = np.zeros(size)
    eps_t = np.ones(size) * eps_r_map[tissue]
    
    # Map tumor mm to grid indices
    t_start = int(t_depth)
    t_end = t_start + int(t_radius * 2)
    if t_end < size:
        eps_t[t_start:t_end] = eps_r_map["Tumor"]
        
    frames = []
    spread = (p_width * 1e-9 / dt) ** 2 
    
    for t in range(s_time):
        # Source (Gaussian Pulse)
        source_val = np.exp(-((t - 100)**2) / spread) * np.sin(2 * np.pi * frequency * 1e9 * t * dt)
        ez_h[5] += source_val
        ez_t[5] += source_val
        
        # Update H and E for HEALTHY
        hy_h[:-1] += 0.5 * (ez_h[1:] - ez_h[:-1])
        ez_h[1:] += (0.5 / eps_h[1:]) * (hy_h[1:] - hy_h[:-1])
        
        # Update H and E for TUMOR
        hy_t[:-1] += 0.5 * (ez_t[1:] - ez_t[:-1])
        ez_t[1:] += (0.5 / eps_t[1:]) * (hy_t[1:] - hy_t[:-1])
        
        # Capture frames every 10 steps to keep the browser responsive
        if t % 10 == 0:
            frames.append(go.Frame(
                data=[
                    go.Scatter(y=ez_h.copy()),
                    go.Scatter(y=ez_t.copy())
                ],
                traces=[0, 1]
            ))
            
    return frames, eps_h, eps_t

# Run the simulation
frames, eps_healthy, eps_tumor = run_dual_fdtd(tissue_type, tumor_depth, tumor_radius, freq, pulse_width, sim_time)

# --- Plotly Side-by-Side Visualization ---
fig = make_subplots(rows=1, cols=2, subplot_titles=(f"Healthy {tissue_type}", f"{tissue_type} + Tumor"))

fig.add_trace(go.Scatter(x=np.arange(size), y=np.zeros(size), name="Healthy E", line=dict(color="#00b4d8")), row=1, col=1)
fig.add_trace(go.Scatter(x=np.arange(size), y=np.zeros(size), name="Tumor E", line=dict(color="#fde725")), row=1, col=2)

# Tumor boundary overlay
t_start = int(tumor_depth)
t_end = t_start + int(tumor_radius * 2)
fig.add_vrect(x0=t_start, x1=t_end, row=1, col=2, fillcolor="red", opacity=0.1, layer="below", line_width=0)

fig.update_layout(
    template="plotly_dark",
    yaxis=dict(range=[-2.2, 2.2], title="E-Field Amplitude"),
    yaxis2=dict(range=[-2.2, 2.2]),
    xaxis=dict(title="Depth (mm)", range=[0, size]),
    xaxis2=dict(title="Depth (mm)", range=[0, size]),
    height=500,
    updatemenus=[dict(
        type="buttons",
        buttons=[dict(label="▶ Play", method="animate", args=[None, {"frame": {"duration": 10, "redraw": False}, "fromcurrent": True}])]
    )]
)

fig.frames = frames
st.plotly_chart(fig, use_container_width=True)

# --- Dielectric Profile Comparison ---
st.subheader("Dielectric Profiles ($\epsilon_r$)")
c1, c2 = st.columns(2)
with c1:
    f_h = go.Figure(data=[go.Scatter(x=np.arange(size), y=eps_healthy, fill='tozeroy', line_color='#00b4d8')])
    f_h.update_layout(template="plotly_dark", height=250, margin=dict(t=20, b=20), xaxis_title="Depth (mm)")
    st.plotly_chart(f_h, use_container_width=True)
with c2:
    f_t = go.Figure(data=[go.Scatter(x=np.arange(size), y=eps_tumor, fill='tozeroy', line_color='#fde725')])
    f_t.add_vrect(x0=t_start, x1=t_end, fillcolor="red", opacity=0.1, layer="below", line_width=0)
    f_t.update_layout(template="plotly_dark", height=250, margin=dict(t=20, b=20), xaxis_title="Depth (mm)")
    st.plotly_chart(f_t, use_container_width=True)
