from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import spatial_router
import uvicorn

app = FastAPI(
    title="Spatial Asset Tracking & Geofencing Engine API",
    description="High-throughput GPS telemetry ingestion and Point-in-Polygon spatial boundary engine.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(spatial_router.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "spatial-asset-geofencing", "spatial_index": "Shapely R-Tree / PostGIS"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
