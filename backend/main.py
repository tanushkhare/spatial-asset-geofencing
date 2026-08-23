from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers.gis import router as gis_router
import uvicorn

app = FastAPI(
    title="Spatial GIS Geo-Analytics Engine API",
    description="Geospatial polygon indexing, spatial bounding queries, and fleet asset clustering.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(gis_router)

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "spatial-gis-engine"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
