# ⚡ Spatial Asset Geofencing

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://spatial-asset-geofencing.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://spatial-asset-geofencing.vercel.app](https://spatial-asset-geofencing.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
Shapely Point-in-Polygon geometric containment engine calculating real-time zone breach tracking, perimeter distances, and alert crossovers.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** Shapely, GeoJSON, PyDeck / Mapbox, FastAPI
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🛡️ Production Standards
* **Resolved PyDeck Bug:** Fixed polygon accessor targeting the actual coordinate structure.
* **Perimeter Alerts:** Detects when GPS points exit authorized boundaries.
* **Multi-Zone Validation:** Evaluates containment across multiple GeoJSON polygons simultaneously.

---

## 🚀 API Contracts
```http
POST /api/v1/spatial/verify
Request:
{
  "asset_id": "ASSET_902",
  "latitude": 37.7800,
  "longitude": -122.4100
}

Response (200 OK):
{
  "inside_zone": true,
  "zone_name": "Downtown Logistics Hub",
  "distance_to_boundary_meters": 42.1,
  "breach_alert": false
}

GET /health
Response: {"status": "healthy"}

💻 Local Quickstart

Bash

pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v