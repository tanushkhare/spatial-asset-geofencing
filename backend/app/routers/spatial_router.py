from fastapi import APIRouter, HTTPException
from backend.app.schemas.spatial_schema import GeofencePolygonCreate, TelemetryPing, GeofenceBreachResponse
from backend.app.services.spatial_service import spatial_engine

router = APIRouter(prefix="/api/v1/spatial", tags=["Geospatial Telemetry & Geofencing"])

@router.post("/geofence", response_model=dict)
async def create_geofence(payload: GeofencePolygonCreate):
    try:
        spatial_engine.add_geofence(
            zone_id=payload.zone_id,
            name=payload.zone_name,
            coords=[tuple(c) for c in payload.coordinates]
        )
        return {"status": "success", "zone_id": payload.zone_id, "message": "Geofence boundary registered."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/telemetry", response_model=GeofenceBreachResponse)
async def ingest_telemetry(payload: TelemetryPing):
    try:
        result = spatial_engine.check_point_containment(
            asset_id=payload.asset_id,
            lng=payload.longitude,
            lat=payload.latitude
        )
        return GeofenceBreachResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/geofences", response_model=dict)
async def list_geofences():
    zones = {k: {"name": v["name"], "coords": v["raw_coords"]} for k, v in spatial_engine.geofences.items()}
    return {"status": "success", "total_zones": len(zones), "zones": zones}
