from pydantic import BaseModel, Field
from typing import List

class GeoSpatialQueryRequest(BaseModel):
    batch_size: int = Field(default=2500, ge=100, le=100000)
    center_latitude: float = Field(default=37.7749)
    center_longitude: float = Field(default=-122.4194)
    radius_km: float = Field(default=15.0)

class SpatialClusterMetric(BaseModel):
    cluster_id: str
    geofence_zone: str
    active_assets_count: int
    density_status: str
    avg_speed_kmh: float

class GeoSpatialQueryResponse(BaseModel):
    total_assets_indexed: int
    spatial_coverage_sq_km: float
    cluster_density_index: str
    query_latency_ms: float
    clusters: List[SpatialClusterMetric]
