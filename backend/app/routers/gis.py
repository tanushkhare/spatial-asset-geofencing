from fastapi import APIRouter
from backend.app.schemas.gis import GeoSpatialQueryRequest, GeoSpatialQueryResponse
from backend.app.services.gis_service import gis_service

router = APIRouter(prefix="/api/v1/gis", tags=["Spatial GIS Analytics Engine"])

@router.post("/query", response_model=GeoSpatialQueryResponse)
async def execute_spatial_query(payload: GeoSpatialQueryRequest):
    return gis_service.process_spatial_query(payload)
