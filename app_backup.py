
import streamlit as st
import pandas as pd
import pydeck as pdk
from quantum_engine import optimize_routes

st.set_page_config(
    page_title="Quantum Flight | QAOA",
    page_icon="🚀",
    layout="wide"
)

if "optimization_history" not in st.session_state:
    st.session_state.optimization_history = []

routes = {
    "Hyderabad → Delhi": 9480,
    "Hyderabad → Mumbai": 8532,
    "Delhi → Mumbai": 9006,
    "Chennai → Bengaluru": 4200,
    "Mumbai → Singapore": 7800,
    "Bengaluru → London": 11500,
    "Delhi → Dubai": 7200,
    "Kolkata → Bangkok": 6500,
    "Chennai → Singapore": 8100,
    "Hyderabad → Bengaluru": 3900,
}

st.markdown("""
<style>
.stApp {
    background: radial-gradient(ellipse at top left, #142c60 0%,
    transparent 45%), linear-gradient(135deg, #050816,
    #091329 60%, #101038);
    color: #eef5ff;
}
.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}
h1, h2, h3 { color: #eaf4ff !important; }
p, label, .stCaption { color: #b8cbe8; }
.hero {
    padding: 30px;
    border: 1px solid #254d85;
    border-radius: 22px;
    background: linear-gradient(120deg,
        rgba(18,43,88,.95), rgba(14,20,53,.92));
    box-shadow: 0 0 30px rgba(0,170,255,.12);
    margin-bottom: 24px;
}
.eyebrow {
    color: #50e6ff;
    letter-spacing: 3px;
    font-size: 12px;
    font-weight: bold;
}
.metric-card {
    background: rgba(13,27,55,.92);
    border: 1px solid #203e6c;
    border-radius: 16px;
    padding: 20px;
    min-height: 115px;
}
.metric-label { color: #91acd1; font-size: 13px; }
.metric-value {
    color: #53e4ff;
    font-size: 27px;
    font-weight: 700;
    margin-top: 8px;
}
.route-card {
    background: rgba(12,25,51,.9);
    border: 1px solid #24446e;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 12px;
}
.route-name {
    color: #54e7ff;
    font-size: 20px;
    font-weight: bold;
}
.route-value {
    color: white;
    font-size: 25px;
    font-weight: bold;
    margin-top: 8px;
}
div.stButton > button {
    background: linear-gradient(90deg,#087cf0,#00c9ed);
    color: white;
    border: 0;
    border-radius: 10px;
    font-weight: bold;
    padding: 12px 22px;
    width: 100%;
}
hr { border-color: #20365b; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="eyebrow">QUANTUM AVIATION LAB / SYSTEM ONLINE</div>
    <h1>✦ Quantum Flight Optimizer</h1>
    
<div style="max-width:900px;margin:20px auto;padding:20px;border:1px solid #00d9ff;border-radius:14px;color:#eafaff;background:rgba(10,20,40,0.85);">
  <h2>⚛️ How It Works</h2>
  <p><b>1. Flight data:</b> Compare 10 sample flight routes and their estimated CO₂ emissions.</p>
  <p><b>2. Quantum optimization:</b> QAOA searches for a route with lower estimated emissions.</p>
  <p><b>3. Route selection:</b> The system displays the route selected by the optimizer.</p>
  <p><b>4. Circuit visualization:</b> Explore a schematic of a 10-qubit quantum circuit.</p>
  <p><i>Technology: Qiskit, QAOA, Python and Streamlit. Runs on a classical simulator.</i></p>
</div>
    <p>Exploring smarter flight paths through quantum
    optimization and sustainable aviation.</p>
    <p>◈ QAOA • Route Intelligence • Carbon Analysis</p>
</div>
""", unsafe_allow_html=True)

st.markdown("### ◈ Mission Overview")
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">SAMPLE ROUTES</div>
        <div class="metric-value">{len(routes)}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">LOWEST SAMPLE EMISSIONS</div>
        <div class="metric-value">{min(routes.values()):,} kg</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">OPTIMIZATION METHOD</div>
        <div class="metric-value">QAOA ⚛</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.markdown("### ✈️ Flight Route Intelligence")

left, right = st.columns([1, 1.15], gap="large")

with left:
    for name, co2 in routes.items():
        st.markdown(f"""
        <div class="route-card">
            <div class="route-name">✦ {name}</div>
            <div class="route-value">{co2:,} kg CO₂</div>
            <div class="metric-label">Illustrative sample emissions</div>
        </div>
        """, unsafe_allow_html=True)

with right:
    st.markdown("#### 📊 Emissions Comparison")
    chart_data = pd.DataFrame({
        "Route": list(routes.keys()),
        "CO₂ (kg)": list(routes.values())
    }).set_index("Route")
    st.bar_chart(chart_data, color="#22c8f5")

st.markdown("---")
st.markdown("### ⚛️ Quantum Optimization Center")
st.write(
    "Run the QAOA demo to select one route from the sample data."
)

if st.button("🚀 ANALYZE FLIGHT PATHS"):
    try:
        with st.spinner("Running quantum optimization..."):
            result = optimize_routes()

        st.session_state.optimization_history.append({
            "Route": result["selected_route"],
            "CO₂ Emissions (kg)": result["emissions"]
        })

        st.success("Optimization finished!")
        st.markdown(
            f"## ✦ Recommended route: {result['selected_route']}"
        )
        st.metric(
            "Estimated CO₂ emissions",
            f"{result['emissions']:,.0f} kg"
        )
        st.metric(
            "Potential savings vs. highest-emission sample",
            f"{max(routes.values()) - result['emissions']:,.0f} kg"
        )
        st.write("Method: QAOA quantum optimization simulation")
        st.write(f"Optimizer status: {result['status']}")
        st.markdown("### ⚛️ Quantum Circuit")
        st.code(result["circuit"], language="text")

    except Exception as e:
        st.error("The optimizer encountered an error.")
        st.code(str(e))

st.markdown("---")
st.markdown("## 🌍 Global Flight Path Visualizer")

flight_paths = [
    {"route": "Hyderabad → Delhi",
     "source": [78.4867, 17.3850],
     "target": [77.1025, 28.6139], "color": [0, 220, 255]},
    {"route": "Hyderabad → Mumbai",
     "source": [78.4867, 17.3850],
     "target": [72.8777, 19.0760], "color": [0, 220, 255]},
    {"route": "Delhi → Mumbai",
     "source": [77.1025, 28.6139],
     "target": [72.8777, 19.0760], "color": [120, 80, 255]},
    {"route": "Chennai → Bengaluru",
     "source": [80.2707, 13.0827],
     "target": [77.5946, 12.9716], "color": [0, 255, 170]},
    {"route": "Mumbai → Singapore",
     "source": [72.8777, 19.0760],
     "target": [103.8198, 1.3521], "color": [120, 80, 255]},
    {"route": "Bengaluru → London",
     "source": [77.5946, 12.9716],
     "target": [-0.1276, 51.5072], "color": [0, 255, 170]},
    {"route": "Delhi → Dubai",
     "source": [77.1025, 28.6139],
     "target": [55.2708, 25.2048], "color": [255, 170, 0]},
    {"route": "Kolkata → Bangkok",
     "source": [88.3639, 22.5726],
     "target": [100.5018, 13.7563], "color": [255, 100, 180]},
    {"route": "Chennai → Singapore",
     "source": [80.2707, 13.0827],
     "target": [103.8198, 1.3521], "color": [0, 220, 255]},
    {"route": "Hyderabad → Bengaluru",
     "source": [78.4867, 17.3850],
     "target": [77.5946, 12.9716], "color": [0, 255, 170]},
]

arc_layer = pdk.Layer(
    "ArcLayer",
    data=flight_paths,
    get_source_position="source",
    get_target_position="target",
    get_source_color="color",
    get_target_color="color",
    get_width=5,
    pickable=True,
)

view = pdk.ViewState(
    latitude=20,
    longitude=75,
    zoom=2,
    pitch=35,
)

deck = pdk.Deck(
    layers=[arc_layer],
    initial_view_state=view,
    map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
    tooltip={"text": "{route}"},
)

st.pydeck_chart(deck, use_container_width=True)

st.markdown("## 📊 Optimization Results History")

if st.session_state.optimization_history:
    st.dataframe(
        st.session_state.optimization_history,
        use_container_width=True
    )
else:
    st.info("Run the optimizer to create your first history record.")

st.caption(
    "Illustrative routes and sample emissions only. "
    "This is not live flight tracking or verified flight-emissions data."
)