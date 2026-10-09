
import streamlit as st
import pandas as pd
import pydeck as pdk
from quantum_engine import optimize_routes

st.set_page_config(
    page_title="Quantum Flight Optimizer",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

ROUTES = {
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

COORDS = {
    "Hyderabad": [78.4867, 17.3850],
    "Delhi": [77.1025, 28.7041],
    "Mumbai": [72.8777, 19.0760],
    "Chennai": [80.2707, 13.0827],
    "Bengaluru": [77.5946, 12.9716],
    "Singapore": [103.8198, 1.3521],
    "London": [-0.1276, 51.5072],
    "Dubai": [55.2708, 25.2048],
    "Kolkata": [88.3639, 22.5726],
    "Bangkok": [100.5018, 13.7563],
}

st.session_state.setdefault("optimization_history", [])
st.session_state.setdefault("latest_result", None)
st.session_state.setdefault("qaoa_error", None)

# Futuristic dashboard styling
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at top left, #142442 0%, transparent 45%),
            linear-gradient(140deg, #070b16 0%, #0b1224 55%, #10172b 100%);
        color: #edf5ff;
    }
    [data-testid="stSidebar"] {
        background: #080e1c;
        border-right: 1px solid #24334e;
    }
    .block-container {
        max-width: 1450px;
        padding-top: 1.7rem;
        padding-bottom: 3rem;
    }
    h1, h2, h3 {
        color: #f1f7ff;
        letter-spacing: -0.5px;
    }
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #111d33, #10172a);
        border: 1px solid #263957;
        padding: 18px;
        border-radius: 16px;
    }
    [data-testid="stMetricLabel"] {
        color: #9fb4d0;
    }
    [data-testid="stMetricValue"] {
        color: #54e4ff;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #087fbd, #6044cf);
        color: white;
        border: 0;
        border-radius: 10px;
        min-height: 44px;
        font-weight: 650;
    }
    div.stButton > button:hover {
        border: 1px solid #63e7ff;
        color: white;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #263957;
        border-radius: 12px;
        overflow: hidden;
    }
    .hero {
        padding: 27px;
        border: 1px solid #294368;
        border-radius: 20px;
        background: linear-gradient(120deg, #142946, #171631);
        margin-bottom: 20px;
    }
    .hero-kicker {
        color: #6be6ff;
        font-size: 0.82rem;
        letter-spacing: 2px;
        font-weight: 700;
    }
    .hero-title {
        font-size: clamp(2rem, 4vw, 3.3rem);
        font-weight: 800;
        line-height: 1.12;
        margin: 10px 0;
    }
    .hero-copy {
        color: #b5c6df;
        max-width: 800px;
        font-size: 1rem;
    }
    .panel {
        padding: 18px;
        border-radius: 15px;
        border: 1px solid #263957;
        background: rgba(16, 27, 48, 0.82);
        margin-bottom: 14px;
    }
    .muted {
        color: #aabbd4;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def show_hero(kicker, title, description):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-kicker">{kicker}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-copy">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_route_data():
    return pd.DataFrame(
        [
            {"Route": route, "Estimated CO₂ (kg)": emissions}
            for route, emissions in ROUTES.items()
        ]
    )


def show_route_map(route_names=None):
    names = list(ROUTES.keys()) if route_names is None else route_names
    rows = []

    for route in names:
        origin, destination = route.split(" → ")
        rows.append(
            {
                "Route": route,
                "CO2": ROUTES[route],
                "source": COORDS[origin],
                "target": COORDS[destination],
            }
        )

    if not rows:
        st.info("No routes match your filters.")
        return

    layer = pdk.Layer(
        "ArcLayer",
        data=rows,
        get_source_position="source",
        get_target_position="target",
        get_source_color=[45, 220, 255],
        get_target_color=[165, 100, 255],
        get_width=3,
        pickable=True,
        auto_highlight=True,
    )

    view = pdk.ViewState(
        latitude=25,
        longitude=62,
        zoom=1.1,
        pitch=25,
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view,
        tooltip={"text": "{Route}\nSample emissions: {CO2} kg"},
        map_style=None,
    )

    st.pydeck_chart(deck, use_container_width=True)


# Sidebar navigation
with st.sidebar:
    st.markdown("## ⚛️ Q-FLIGHT")
    st.caption("QUANTUM AVIATION LAB")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "Flight Explorer",
            "Quantum Lab",
            "Analytics",
            "Reports",
        ],
    )

    st.divider()
    st.caption("BUILT WITH")
    st.markdown("Python · Streamlit · Qiskit")
    st.caption("Prototype • Sample emissions data")


data = get_route_data()
history = st.session_state.optimization_history
latest = st.session_state.latest_result


# PAGE 1: OVERVIEW
if page == "Overview":
    show_hero(
        "QUANTUM-ASSISTED AVIATION",
        "Quantum Flight Optimizer ✈️",
        "Explore sample flight routes and experiment with QAOA, "
        "a quantum optimization algorithm, to investigate lower-emission choices.",
    )

    best_sample = data.loc[data["Estimated CO₂ (kg)"].idxmin()]
    highest_sample = data["Estimated CO₂ (kg)"].max()

    a, b, c, d = st.columns(4)
    a.metric("Routes in dataset", len(ROUTES))
    b.metric("Lowest sample estimate", f'{best_sample["Estimated CO₂ (kg)"]:,} kg')
    c.metric("Highest sample estimate", f"{highest_sample:,} kg")
    d.metric("QAOA runs completed", len(history))

    st.subheader("✦ Flight network")
    st.markdown(
        '<div class="muted">Illustrative connections between cities, '
        'not live flight tracking.</div>',
        unsafe_allow_html=True,
    )
    show_route_map()

    left, right = st.columns([1.2, 1])

    with left:
        st.subheader("Route emissions overview")
        chart = data.sort_values("Estimated CO₂ (kg)").set_index("Route")
        st.bar_chart(chart)

    with right:
        st.subheader("Latest optimization")
        if latest:
            st.success("A QAOA result is available.")
            st.markdown(f"**Selected route:** {latest['selected_route']}")
            st.metric("Result emissions", f"{latest['emissions']:,.0f} kg")
            st.caption(f"Optimizer status: {latest['status']}")
            st.info("Open Quantum Lab to run another optimization.")
        else:
            st.info("No optimization run yet.")
            st.markdown(
                "Open **Quantum Lab** and press **Run QAOA optimization** "
                "to generate a result."
            )

    st.caption(
        "All emissions values are illustrative sample data, not verified "
        "measurements for real flights."
    )


# PAGE 2: FLIGHT EXPLORER
elif page == "Flight Explorer":
    show_hero(
        "EXPLORE THE NETWORK",
        "Flight Explorer 🌍",
        "Search routes, filter by sample emissions, inspect individual routes, "
        "and explore an illustrative flight map.",
    )

    left, right = st.columns([1.4, 1])
    with left:
        search = st.text_input(
            "Search origin or destination",
            placeholder="Try Hyderabad, London, Singapore...",
        )
    with right:
        limit = st.slider(
            "Maximum sample emissions (kg)",
            min_value=min(ROUTES.values()),
            max_value=max(ROUTES.values()),
            value=max(ROUTES.values()),
            step=100,
        )

    filtered = data[
        data["Route"].str.contains(search, case=False, na=False)
        & (data["Estimated CO₂ (kg)"] <= limit)
    ]

    st.subheader(f"Matching routes: {len(filtered)}")
    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.subheader("Route map")
    show_route_map(filtered["Route"].tolist())

    st.subheader("Route details")
    selected = st.selectbox("Choose a route", list(ROUTES.keys()))
    origin, destination = selected.split(" → ")
    x, y, z = st.columns(3)
    x.metric("Sample emissions", f"{ROUTES[selected]:,} kg")
    y.metric("Origin", origin)
    z.metric("Destination", destination)

    st.caption(
        "These emissions values are sample estimates for demonstration "
        "and should not be used for real travel decisions."
    )


# PAGE 3: QUANTUM LAB
elif page == "Quantum Lab":
    show_hero(
        "OPTIMIZATION WORKBENCH",
        "Quantum Lab ⚛️",
        "Run your QAOA prototype and inspect the result and a schematic "
        "quantum-circuit visualization.",
    )

    st.markdown(
        """
        <div class="panel">
            <b>Optimization goal</b><br>
            Choose one route variable while minimizing its sample-emissions cost.
            <br><br>
            <span class="muted">
            QAOA runs on a classical statevector simulator in this project.
            The displayed circuit is a schematic, not the exact internal QAOA circuit.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Run optimization")
    run_clicked = st.button(
        "⚛️ RUN QAOA OPTIMIZATION",
        type="primary",
        use_container_width=True,
    )

    if run_clicked:
        try:
            with st.spinner(
                "Running QAOA on the classical simulator. This may take a while..."
            ):
                result = optimize_routes()

            st.session_state.latest_result = result
            st.session_state.qaoa_error = None
            st.session_state.optimization_history.append(
                {
                    "Run": len(st.session_state.optimization_history) + 1,
                    "Selected route": result["selected_route"],
                    "Estimated CO₂ (kg)": result["emissions"],
                    "Status": result["status"],
                    "Method": "QAOA on classical simulator",
                }
            )
            st.success("Optimization finished!")
        except Exception as error:
            st.session_state.qaoa_error = str(error)

    if st.session_state.qaoa_error:
        st.error("The optimizer encountered an error.")
        st.code(st.session_state.qaoa_error)

    latest = st.session_state.latest_result

    if latest:
        st.divider()
        st.subheader("✦ Optimization result")

        left, right = st.columns(2)
        with left:
            st.metric("Recommended route", latest["selected_route"] or "No route returned")
        with right:
            st.metric("Estimated CO₂", f'{latest["emissions"]:,.0f} kg')

        st.caption(f"Optimizer status: {latest['status']}")
        st.info(
            "QAOA is heuristic. One run does not prove that the global optimum "
            "was found."
        )

        st.subheader("Circuit visualization")
        st.caption("Schematic circuit for learning and presentation.")
        st.code(latest.get("circuit", "No circuit visualization was returned."), language="text")

    else:
        st.info("Your results will appear here after a successful run.")


# PAGE 4: ANALYTICS
elif page == "Analytics":
    show_hero(
        "DATA & INSIGHTS",
        "Emissions Analytics 📊",
        "Compare the illustrative route values and inspect which sample routes "
        "have the lowest and highest values.",
    )

    ordered = data.sort_values("Estimated CO₂ (kg)", ascending=True)
    low = ordered.iloc[0]
    high = ordered.iloc[-1]

    a, b = st.columns(2)
    a.metric("Lowest sample route", low["Route"])
    b.metric("Highest sample route", high["Route"])

    st.subheader("All routes, lowest to highest")
    st.bar_chart(ordered.set_index("Route"))
    st.dataframe(ordered, use_container_width=True, hide_index=True)

    if latest:
        st.subheader("Most recent QAOA result")
        st.write(f"**Selected route:** {latest['selected_route']}")
        st.write(f"**Sample emissions:** {latest['emissions']:,.0f} kg")
        st.write(f"**Status:** {latest['status']}")
    else:
        st.info("Run QAOA in Quantum Lab to add an optimization result.")

    st.caption(
        "The chart compares supplied sample values. It does not establish "
        "actual airline emissions or guaranteed savings."
    )


# PAGE 5: REPORTS
elif page == "Reports":
    show_hero(
        "EXPORT & REVIEW",
        "Reports Center 📁",
        "Review completed QAOA runs and download their results for your project presentation.",
    )

    history = st.session_state.optimization_history

    if history:
        history_df = pd.DataFrame(history)
        st.subheader("Optimization history")
        st.dataframe(history_df, use_container_width=True, hide_index=True)

        csv_data = history_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ DOWNLOAD RUN HISTORY (CSV)",
            data=csv_data,
            file_name="quantum_flight_optimizer_report.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.info(
            "No runs have been recorded in this session yet. "
            "Go to Quantum Lab and run the optimizer first."
        )

    st.divider()
    st.subheader("Dataset")
    st.write("The current prototype contains 10 illustrative city-to-city routes.")
    st.download_button(
        "⬇️ DOWNLOAD SAMPLE ROUTES (CSV)",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="sample_flight_routes.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.caption(
        "Run history is kept in the current Streamlit session. Download it "
        "to keep a copy before closing or restarting the app."
    )