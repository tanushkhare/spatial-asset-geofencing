from pydantic import BaseModel, Field
from typing import List, Tuple, Dict, Any, Optional
from datetime import datetime

class GeofencePolygonCreate(BaseModel):
    zone_id: str = Field(..., description="Unique zone identifier")
    zone_name: str
    coordinates: List[Tuple[float, float]] = Field(..., min_length=3, description="List of (longitude, latitude) polygon vertices")

class TelemetryPing(BaseModel):
    asset_id: str = Field(..., description="Mobile asset identifier (e.g. TRUCK-401)")
    longitude: float = Field(..., ge=-180.0, le=180.0)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    speed_kmh: Optional[float] = Field(default=0.0, ge=0.0)

class GeofenceBreachResponse(BaseModel):
    asset_id: str
    latitude: float
    longitude: float
    inside_geofence: bool
    active_zones: List[str]
    alert_status: str
    timestamp: str
