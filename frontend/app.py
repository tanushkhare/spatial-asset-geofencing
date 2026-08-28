import streamlit as st
import requests
import pydeck as pdk
import pandas as pd

st.set_page_config(page_title="Spatial Asset Geofencing Platform", layout="wide")

st.title("🛰️ High-Throughput Spatial Asset Geofencing Platform")
st.markdown("Real-time GPS coordinate telemetry ingestion with computational Point-in-Polygon containment checks.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Asset GPS Telemetry Ingest")
    asset_id = st.text_input("Asset Identifier", value="FLEET-TRUCK-88")
    
    c1, c2 = st.columns(2)
    with c1:
        lat = st.number_input("Latitude", value=37.7900, format="%.6f")
    with c2:
        lng = st.number_input("Longitude", value=-122.4100, format="%.6f")
        
    speed = st.slider("Vehicle Speed (km/h)", 0, 140, 45)

    if st.button("Evaluate Geofence Containment", type="primary"):
        with st.spinner("Computing Shapely spatial polygon intersection..."):
            try:
                res = requests.post("http://localhost:8000/api/v1/spatial/evaluate", json={"asset_id": asset_id, "latitude": lat, "longitude": lng, "speed_kmh": speed}, timeout=5)
                if res.status_code == 200:
                    st.session_state["p19_result"] = res.json()
                    st.success("Containment Calculated!")
                else:
                    st.error(f"API Error: {res.text}")
            except Exception:
                st.warning("Backend offline. Executing client-side fallback computation.")
                is_inside = (-122.42 <= lng <= -122.40) and (37.78 <= lat <= 37.80)
                st.session_state["p19_result"] = {
                    "asset_id": asset_id,
                    "latitude": lat,
                    "longitude": lng,
                    "inside_geofence": is_inside,
                    "active_zones": ["San Francisco Logistics Port"] if is_inside else [],
                    "alert_status": "RESTRICTED PERIMETER INTRUSION DETECTED" if is_inside else "AUTHORIZED / OUTSIDE GEOFENCE",
                    "timestamp": "2026-08-28T07:30:00Z"
                }

with col2:
    if "p19_result" in st.session_state:
        res = st.session_state["p19_result"]
        st.subheader("Perimeter Breach Telemetry")
        
        m1, m2 = st.columns(2)
        m1.metric("Asset ID", res["asset_id"])
        status_color = "red" if res["inside_geofence"] else "green"
        m2.metric("Containment Status", "INSIDE PERIMETER" if res["inside_geofence"] else "CLEAR", delta=res["alert_status"])
        
        if res["active_zones"]:
            st.error(f"⚠️ Active Zones Breached: {', '.join(res['active_zones'])}")
        else:
            st.success("✅ Asset operates within authorized geographical bounds.")
            
        # Map visualization with PyDeck
        asset_df = pd.DataFrame([{"lat": res["latitude"], "lon": res["longitude"], "name": res["asset_id"]}])
        
        geofence_polygon = [
            [-122.42, 37.78],
            [-122.40, 37.78],
            [-122.40, 37.80],
            [-122.42, 37.80],
            [-122.42, 37.78]
        ]
        
        poly_df = pd.DataFrame([{"polygon": geofence_polygon, "name": "San Francisco Logistics Port"}])
        
        polygon_layer = pdk.Layer(
            "PolygonLayer",
            poly_df,
            get_polygon="polygon",
            get_fill_color=[255, 0, 0, 60] if res["inside_geofence"] else [0, 255, 0, 40],
            get_line_color=[255, 0, 0] if res["inside_geofence"] else [0, 255, 0],
            line_width_min_pixels=2,
            pickable=True
        )
        
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            asset_df,
            get_position=["lon", "lat"],
            get_color=[255, 255, 0],
            get_radius=80,
            pickable=True
        )
        
        view_state = pdk.ViewState(latitude=res["latitude"], longitude=res["longitude"], zoom=13, pitch=0)
        st.pydeck_chart(pdk.Deck(layers=[polygon_layer, scatter_layer], initial_view_state=view_state))
