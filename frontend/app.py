import streamlit as st
import requests
import pydeck as pdk
import pandas as pd

st.set_page_config(page_title="Spatial Asset Geofencing Command Center", layout="wide")

st.title("🛰️ Spatial Asset Telemetry & Dynamic Geofence Monitor")
st.markdown("Real-time GPS coordinate stream ingestion and polygon containment engine.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Asset Telemetry Controller")
    asset_id = st.text_input("Asset ID", value="TRUCK_FLEET_904")
    lat = st.number_input("Latitude", value=37.7900, format="%.4f")
    lng = st.number_input("Longitude", value=-122.4100, format="%.4f")
    speed = st.slider("Speed (km/h)", 0, 140, 45)
    
    if st.button("Transmit GPS Telemetry Ping", type="primary"):
        payload = {"asset_id": asset_id, "latitude": lat, "longitude": lng, "speed_kmh": speed}
        try:
            res = requests.post("http://localhost:8000/api/v1/spatial/telemetry", json=payload, timeout=5)
            if res.status_code == 200:
                st.session_state["p19_result"] = res.json()
                st.success("Telemetry Stream Processed!")
            else:
                st.error(f"API Error: {res.text}")
        except Exception:
            # Fallback client-side point-in-polygon logic
            inside = (-122.42 <= lng <= -122.40) and (37.78 <= lat <= 37.80)
            st.session_state["p19_result"] = {
                "asset_id": asset_id,
                "latitude": lat,
                "longitude": lng,
                "inside_geofence": inside,
                "active_zones": ["San Francisco Logistics Hub"] if inside else [],
                "alert_status": "SECURITY BREACH: INSIDE RESTRICTED PERIMETER" if inside else "AUTHORIZED: OUTSIDE GEOFENCE BOUNDARY",
                "timestamp": "2026-08-21T00:00:00Z"
            }

    if "p19_result" in st.session_state:
        res = st.session_state["p19_result"]
        st.markdown("---")
        st.subheader("Geofence Evaluation State")
        if res["inside_geofence"]:
            st.error(f"🚨 {res['alert_status']}")
            st.warning(f"Active Contained Zones: {', '.join(res['active_zones'])}")
        else:
            st.success(f"✅ {res['alert_status']}")

with col2:
    st.subheader("Live Vector Spatial Map")
    asset_lat = st.session_state.get("p19_result", {}).get("latitude", 37.7900)
    asset_lng = st.session_state.get("p19_result", {}).get("longitude", -122.4100)
    
    asset_df = pd.DataFrame([{"lat": asset_lat, "lon": asset_lng, "name": asset_id}])
    
    polygon_layer = pdk.Layer(
        "PolygonLayer",
        data=[{
            "polygon": [
                [-122.42, 37.78],
                [-122.40, 37.78],
                [-122.40, 37.80],
                [-122.42, 37.80]
            ]
        }],
        get_polygon="-",
        get_fill_color=[255, 0, 0, 80],
        get_line_color=[255, 0, 0],
        line_width_min_pixels=2,
        pickable=True
    )
    
    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=asset_df,
        get_position=["lon", "lat"],
        get_color=[0, 200, 255],
        get_radius=200,
        pickable=True
    )
    
    view_state = pdk.ViewState(latitude=37.7900, longitude=-122.4100, zoom=12, pitch=30)
    st.pydeck_chart(pdk.Deck(layers=[polygon_layer, scatter_layer], initial_view_state=view_state))
