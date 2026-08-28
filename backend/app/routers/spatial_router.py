from fastapi import APIRouter, HTTPException
from backend.app.schemas.spatial_schema import GeofencePolygonCreate, TelemetryPing, GeofenceBreachResponse
from backend.app.services.spatial_service import spatial_engine

router = APIRouter(prefix="/api/v1/spatial", tags=["Geospatial Telemetry & Geofencing"])

@router.post("/geofence")
async def create_geofence(payload: GeofencePolygonCreate):
    try:
        spatial_engine.add_geofence(payload.zone_id, payload.zone_name, [tuple(c) for c in payload.coordinates])
        return {"status": "SUCCESS", "zone_id": payload.zone_id, "message": "Geofence boundary registered."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/evaluate", response_model=GeofenceBreachResponse)
async def evaluate_ping(payload: TelemetryPing):
    try:
        result = spatial_engine.evaluate_containment(payload.asset_id, payload.longitude, payload.latitude)
        return GeofenceBreachResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geofences")
async def list_geofences():
    zones = {k: {"name": v["name"], "coords": v["raw_coords"]} for k, v in spatial_engine.geofences.items()}
    return {"status": "SUCCESS", "total_zones": len(zones), "zones": zones}
