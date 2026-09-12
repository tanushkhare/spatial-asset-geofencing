# ⚡ Spatial Asset Geofencing

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://spatial-asset-geofencing.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://spatial-asset-geofencing.vercel.app](https://spatial-asset-geofencing.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
Computational geometry engine calculating point-in-polygon containment and breach crossover alerts.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** Shapely, GeoJSON, PyDeck, FastAPI
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🚀 API Contracts
```http
POST /api/v1/spatial/verify
GET /health
```

---

## 💻 Local Quickstart
```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v
```
