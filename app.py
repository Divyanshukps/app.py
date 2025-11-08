import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import plotly.graph_objects as go

st.set_page_config(page_title="AI-Powered Smart Waste Management", layout="wide")

st.title("♻️ AI-Powered Smart Waste Management and Recycling Assistant")
st.write("Interactive demo dashboard — city waste metrics, predictions, anomaly alerts and recycling tips.")

# --- Sample Data ---
sample_data = {
    "city": "Sample City",
    "today_waste_tons": 15.2,
    "predicted_tomorrow_tons": 16.4,
    "recycling_rate": 45,
    "daily": [8, 9, 10, 12, 13, 14, 15],
    "dates": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    "bins": [
        {"id": "Bin 1", "lat": 40.7128, "lon": -74.0060, "fill_pct": 85},
        {"id": "Bin 2", "lat": 40.7158, "lon": -74.0020, "fill_pct": 60},
        {"id": "Bin 3", "lat": 40.7108, "lon": -74.0120, "fill_pct": 95},
    ]
}

# --- Metrics ---
col1, col2, col3 = st.columns(3)
col1.metric("Today's Waste", f"{sample_data['today_waste_tons']} tons")
col2.metric("Bins Overflowing", sum(b['fill_pct'] > 80 for b in sample_data['bins']))
col3.metric("Predicted Waste (Tomorrow)", f"{sample_data['predicted_tomorrow_tons']} tons")

st.divider()

# --- Chart (Plotly) ---
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=sample_data["dates"],
    y=sample_data["daily"],
    fill='tozeroy',
    name='Waste (tons)',
    line=dict(color="#3b82f6")
))
fig.update_layout(
    paper_bgcolor="#0f1724",
    plot_bgcolor="#111827",
    font=dict(color="#cbd5e1"),
    margin=dict(l=40, r=20, t=30, b=30),
)
st.plotly_chart(fig, use_container_width=True)

# --- Map (Folium) ---
m = folium.Map(location=[40.7138, -74.0060], zoom_start=13)
for b in sample_data["bins"]:
    popup = f"{b['id']}<br>Fill: {b['fill_pct']}%"
    color = "red" if b["fill_pct"] > 90 else "orange" if b["fill_pct"] > 80 else "green"
    folium.CircleMarker(
        location=[b["lat"], b["lon"]],
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        popup=popup
    ).add_to(m)

st.subheader("🗺️ Waste Distribution Map")
st_folium(m, width=700, height=400)

# --- Recycling Tips ---
st.subheader("♻️ Recycling Tips")
st.markdown("""
- Separate recyclables from general waste  
- Rinse containers before recycling  
- Recycle paper, plastic, glass, and metal  
""")

# --- Anomaly Alerts ---
st.subheader("⚠️ Anomaly Alerts")
for b in sample_data["bins"]:
    if b["fill_pct"] > 90:
        st.error(f"{b['id']} is critically full ({b['fill_pct']}%). Schedule immediate pickup.")
