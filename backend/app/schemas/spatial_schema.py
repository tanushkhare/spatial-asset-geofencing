from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from datetime import datetime

class GeofencePolygonCreate(BaseModel):
    zone_id: str = Field(..., description="Unique zone identifier (e.g. airport_hub, port_terminal)")
    zone_name: str
    coordinates: List[Tuple[float, float]] = Field(
        ..., min_length=3, description="List of (longitude, latitude) polygon boundary vertices"
    )

class TelemetryPing(BaseModel):
    asset_id: str
    longitude: float = Field(..., ge=-180.0, le=180.0)
    latitude: float = Field(..., ge=-90.0, le=90.0)
    speed_kmh: float = Field(default=0.0, ge=0.0)
    timestamp: Optional[datetime] = None

class GeofenceBreachResponse(BaseModel):
    asset_id: str
    latitude: float
    longitude: float
    inside_geofence: bool
    active_zones: List[str]
    alert_status: str
    timestamp: datetime
