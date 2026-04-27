import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.header("1D FDTD Microwave Simulation")

# Sidebar Controls
with st.sidebar:
    st.subheader("Simulation Parameters")
    tissue_type = st.selectbox("Tissue Library", ["Fat", "Skin"])
    freq = st.slider("Frequency (GHz)", 1.0, 10.0, 2.4)
    tumor_depth = st.slider("Tumor Depth (cm)", 1, 10, 5)
    tumor_radius = st.slider("Tumor Radius (cm)", 0.5, 2.0, 1.0)

# Constants
eps_r_map = {"Fat": 5.3, "Skin": 37, "Tumor": 55}
c0 = 3e8
dx = 0.001  # 1mm spatial step
size = 200  # grid size
dt = dx / (2 * c0)  # CFL condition

# Simulation Engine
def run_fdtd():
    ez = np.zeros(size)
    hy = np.zeros(size)
    
    # Material Profile
    eps = np.ones(size) * eps_r_map[tissue_type]
    t_start = int(tumor_depth * 10)
    t_end = t_start + int(tumor_radius * 10)
    eps[t_start:t_end] = eps_r_map["Tumor"]
    
    frames = []
    for t in range(300):
        # Source (Gaussian Pulse)
        ez[5] += np.exp(-((t - 30)**2) / 100) * np.sin(2 * np.pi * freq * 1e9 * t * dt)
        
        # Update H and E
        hy[:-1] += 0.5 * (ez[1:] - ez[:-1])
        ez[1:] += (0.5 / eps[1:]) * (hy[1:] - hy[:-1])
        
        if t % 10 == 0:
            frames.append(go.Frame(data=[go.Scatter(x=np.arange(size), y=ez.copy())]))
            
    return frames, eps

frames, eps_profile = run_fdtd()

fig = go.Figure(
    data=[go.Scatter(x=np.arange(size), y=np.zeros(size), name="E-Field")],
    layout=go.Layout(
        xaxis=dict(title="Grid Position (mm)"),
        yaxis=dict(range=[-1.5, 1.5], title="Amplitude"),
        updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None])])]
    ),
    frames=frames
)
fig.update_layout(template="plotly_dark", colorway=['#440154'])
st.plotly_chart(fig, use_container_width=True)
