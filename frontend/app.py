import streamlit as st
import pandas as pd
import urllib.request
import json

# =========================================================
# AURA — Adaptive Urban Road Intelligence & Response Assistant
# =========================================================

st.set_page_config(
    page_title="AURA | Urban Traffic Intelligence",
    page_icon="🚦",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:5000/api/traffic"

# =========================================================
# PROFESSIONAL STYLING
# =========================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
    max-width: 1500px;
}

.aura-header {
    padding: 24px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.25);
    margin-bottom: 20px;
}

.aura-title {
    font-size: 40px;
    font-weight: 800;
}

.aura-subtitle {
    font-size: 18px;
    opacity: 0.75;
}

.status-online {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 20px;
    border: 1px solid rgba(0,180,80,0.4);
    font-size: 13px;
    font-weight: 700;
}

.section-title {
    font-size: 22px;
    font-weight: 750;
    margin-top: 15px;
    margin-bottom: 12px;
}

.decision-panel {
    padding: 22px;
    border-radius: 14px;
    border: 1px solid rgba(128,128,128,0.3);
    margin: 10px 0 20px 0;
}

.decision-title {
    font-size: 20px;
    font-weight: 800;
}

.decision-text {
    font-size: 15px;
    line-height: 1.6;
}

.footer {
    text-align: center;
    opacity: 0.6;
    padding: 20px;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD BACKEND DATA
# =========================================================

@st.cache_data(ttl=5)
def load_traffic_data():

    try:
        with urllib.request.urlopen(
            API_URL,
            timeout=5
        ) as response:

            data = json.loads(
                response.read().decode()
            )

        return pd.DataFrame(data)

    except Exception:
        return pd.DataFrame()


df = load_traffic_data()

# =========================================================
# BACKEND CONNECTION CHECK
# =========================================================

if df.empty:

    st.error("⚠️ AURA backend is unavailable.")

    st.info(
        "Start the Flask backend with: "
        "`python backend\\app.py`"
    )

    st.stop()

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="aura-header">

<div class="aura-title">
🚦 AURA
</div>

<div class="aura-subtitle">
Adaptive Urban Road Intelligence & Response Assistant
</div>

<br>

<div class="status-online">
● SYSTEM ONLINE
</div>

<br><br>

Intelligent decision support for detecting traffic risk,
forecasting conditions, recommending interventions,
and evaluating what-if scenarios.

</div>
""", unsafe_allow_html=True)

st.caption(
    "🚦 Detect  •  📊 Analyze  •  ⚠️ Assess Risk  •  "
    "🤖 Recommend  •  🧪 Simulate"
)

# =========================================================
# CRITICAL ALERT
# =========================================================

critical_roads = df[
    df["priority"] == "CRITICAL"
]

if not critical_roads.empty:

    critical_road = critical_roads.sort_values(
        by="risk_score",
        ascending=False
    ).iloc[0]

    st.error(
        f"""
🚨 **CRITICAL TRAFFIC ALERT — {critical_road['road']}**

Traffic: {int(critical_road['vehicle_count'])} vehicles  
Speed: {int(critical_road['avg_speed'])} km/h  
Capacity: {int(critical_road['road_capacity'])} vehicles  
Occupancy: {critical_road['occupancy']:.1f}%  
Risk Score: {critical_road['risk_score']:.2f}

**Recommended action:** {critical_road['recommended_action']}
"""
    )

else:

    st.success(
        "✅ No critical traffic conditions detected."
    )

# =========================================================
# NETWORK COMMAND CENTER
# =========================================================

st.markdown(
    '<div class="section-title">🌐 Network Command Center</div>',
    unsafe_allow_html=True
)

total_vehicles = int(
    df["vehicle_count"].sum()
)

average_speed = df["avg_speed"].mean()

critical_count = int(
    (df["priority"] == "CRITICAL").sum()
)

high_risk_count = int(
    (df["priority"] == "HIGH").sum()
)

highest_risk_row = df.loc[
    df["risk_score"].idxmax()
]

highest_risk_road = highest_risk_row["road"]
highest_risk_score = highest_risk_row["risk_score"]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🚗 Network Traffic",
        f"{total_vehicles}"
    )

with col2:
    st.metric(
        "⚡ Average Speed",
        f"{average_speed:.1f} km/h"
    )

with col3:
    st.metric(
        "🚨 Critical Roads",
        critical_count
    )

with col4:
    st.metric(
        "🎯 Highest Risk",
        f"{highest_risk_road}",
        delta=f"{highest_risk_score:.2f}"
    )

# =========================================================
# ROAD SELECTION
# =========================================================

st.markdown(
    '<div class="section-title">📍 Road Intelligence</div>',
    unsafe_allow_html=True
)

road = st.selectbox(
    "Select a road segment to investigate",
    df["road"].tolist()
)

selected = df[
    df["road"] == road
].iloc[0]

# =========================================================
# SELECTED ROAD STATUS
# =========================================================

st.markdown(
    f"### {road} — Live Intelligence"
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Traffic Volume",
        f"{int(selected['vehicle_count'])} vehicles"
    )

with c2:
    st.metric(
        "Road Capacity",
        f"{int(selected['road_capacity'])} vehicles"
    )

with c3:
    st.metric(
        "Occupancy",
        f"{selected['occupancy']:.1f}%"
    )

with c4:
    st.metric(
        "Average Speed",
        f"{int(selected['avg_speed'])} km/h"
    )

# =========================================================
# INCIDENT + PRIORITY
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:

    if int(selected["incident_flag"]) == 1:
        st.error("🚨 INCIDENT DETECTED")
    else:
        st.success("✅ NO INCIDENT")

with c2:

    if selected["priority"] == "CRITICAL":
        st.error(f"🚨 PRIORITY: {selected['priority']}")

    elif selected["priority"] == "HIGH":
        st.warning(f"⚠️ PRIORITY: {selected['priority']}")

    elif selected["priority"] == "MEDIUM":
        st.info(f"ℹ️ PRIORITY: {selected['priority']}")

    else:
        st.success(f"✅ PRIORITY: {selected['priority']}")

with c3:

    st.metric(
        "Risk Score",
        f"{selected['risk_score']:.2f}"
    )

# =========================================================
# AURA DECISION SUPPORT
# =========================================================

st.markdown(
    '<div class="section-title">🧠 AURA Decision Support</div>',
    unsafe_allow_html=True
)

st.markdown(
    f"""
<div class="decision-panel">

<div class="decision-title">
🤖 Recommended Response
</div>

<br>

<div class="decision-text">

<b>Situation:</b>
{selected['congestion_level']} congestion detected on {road}.

<br><br>

<b>Traffic:</b>
{int(selected['vehicle_count'])} vehicles /
{int(selected['road_capacity'])} vehicle capacity.

<br><br>

<b>Occupancy:</b>
{selected['occupancy']:.1f}%

<br><br>

<b>Risk Score:</b>
{selected['risk_score']:.2f}

<br><br>

<b>Priority:</b>
{selected['priority']}

<br><br>

<b>Recommended Action:</b>
{selected['recommended_action']}

</div>

</div>
""",
    unsafe_allow_html=True
)

# =========================================================
# NETWORK TRAFFIC
# =========================================================

st.markdown(
    '<div class="section-title">📊 Traffic Across Network</div>',
    unsafe_allow_html=True
)

chart_data = df.set_index(
    "road"
)[["vehicle_count"]]

st.bar_chart(
    chart_data,
    width="stretch"
)

# =========================================================
# NETWORK INTELLIGENCE TABLE
# =========================================================

display_df = df[
    [
        "road",
        "vehicle_count",
        "road_capacity",
        "occupancy",
        "avg_speed",
        "congestion_level",
        "risk_score",
        "priority",
        "incident_flag"
    ]
].copy()

display_df.columns = [
    "Road",
    "Vehicles",
    "Capacity",
    "Occupancy %",
    "Avg Speed",
    "Congestion",
    "Risk Score",
    "Priority",
    "Incident"
]

display_df["Incident"] = display_df["Incident"].map({
    0: "No",
    1: "Yes"
})

st.dataframe(
    display_df,
    width="stretch",
    hide_index=True
)

# =========================================================
# TRAFFIC FORECAST
# =========================================================

st.markdown(
    '<div class="section-title">📈 Traffic Forecast</div>',
    unsafe_allow_html=True
)

current_traffic = int(
    selected["vehicle_count"]
)

forecast_data = pd.DataFrame({

    "Time": [
        "Now",
        "15 min",
        "30 min",
        "60 min"
    ],

    "Traffic Load": [
        current_traffic,
        current_traffic * 1.05,
        current_traffic * 1.10,
        current_traffic * 1.15
    ]

})

st.line_chart(
    forecast_data.set_index("Time"),
    width="stretch"
)

st.caption(
    f"Estimated traffic trend for {road}. "
    "Forecast values are simulated demonstration estimates."
)

# =========================================================
# SPILLBACK RISK
# =========================================================

st.markdown(
    '<div class="section-title">🔗 Spillback Risk</div>',
    unsafe_allow_html=True
)

spillback_df = df[
    [
        "road",
        "vehicle_count",
        "road_capacity",
        "risk_score",
        "priority"
    ]
].copy()

spillback_df.columns = [
    "Road",
    "Traffic Load",
    "Capacity",
    "Risk Score",
    "Priority"
]

st.dataframe(
    spillback_df,
    width="stretch",
    hide_index=True
)

if selected["priority"] in [
    "CRITICAL",
    "HIGH"
]:

    st.warning(
        f"⚠️ Elevated network risk detected around {road}. "
        "Connected road segments should be monitored."
    )

else:

    st.success(
        f"✅ {road} currently has no critical spillback warning."
    )

# =========================================================
# WHAT-IF SIMULATION
# =========================================================

st.markdown(
    '<div class="section-title">🧪 What-if Simulation</div>',
    unsafe_allow_html=True
)

st.write(
    "Evaluate the estimated impact of a possible "
    "traffic intervention before taking action."
)

diversion = st.slider(
    "Simulated Traffic Diversion (%)",
    min_value=0,
    max_value=50,
    value=20
)

simulate = st.button(
    "🚀 Run Intervention Simulation",
    width="stretch"
)

if simulate:

    current_load = int(
        selected["vehicle_count"]
    )

    current_risk = float(
        selected["risk_score"]
    )

    simulated_load = (
        current_load *
        (1 - diversion / 100)
    )

    improvement = (
        current_load -
        simulated_load
    )

    improvement_percent = (
        improvement /
        current_load
    ) * 100

    simulated_risk = (
        current_risk *
        (1 - diversion / 100)
    )

    st.markdown(
        "### 📊 Intervention Impact"
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric(
            "Current Traffic",
            f"{current_load:.0f}"
        )

    with s2:
        st.metric(
            "Simulated Traffic",
            f"{simulated_load:.0f}",
            delta=f"-{improvement:.0f}"
        )

    with s3:
        st.metric(
            "Traffic Reduction",
            f"{improvement_percent:.1f}%"
        )

    with s4:
        st.metric(
            "Simulated Risk",
            f"{simulated_risk:.2f}",
            delta=f"-{current_risk - simulated_risk:.2f}"
        )

    st.success(
        f"""
✅ **Scenario Result**

A simulated **{diversion}% diversion** could reduce
traffic on **{road}** from approximately
**{current_load} → {simulated_load:.0f} vehicles**.

Estimated risk changes from
**{current_risk:.2f} → {simulated_risk:.2f}**.
"""
    )

    st.info(
        "💡 This is a simulated decision-support scenario. "
        "It does not directly control real-world traffic infrastructure."
    )

# =========================================================
# AURA INTELLIGENCE PIPELINE
# =========================================================

st.divider()

st.markdown(
    '<div class="section-title">⚙️ AURA Intelligence Pipeline</div>',
    unsafe_allow_html=True
)

p1, p2, p3, p4, p5 = st.columns(5)

with p1:
    st.markdown("### 🚗")
    st.write("Traffic Data")

with p2:
    st.markdown("### 📊")
    st.write("Analytics")

with p3:
    st.markdown("### ⚠️")
    st.write("Risk Assessment")

with p4:
    st.markdown("### 🤖")
    st.write("Recommendation")

with p5:
    st.markdown("### 🧪")
    st.write("Simulation")

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
<div class="footer">

<b>AURA</b> — Adaptive Urban Road Intelligence & Response Assistant

<br><br>

Decision-support prototype for urban traffic intelligence.

<br>

Analytics-derived and simulated outputs do not directly
control real-world traffic infrastructure.

</div>
""",
    unsafe_allow_html=True
)