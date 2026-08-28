from shapely.geometry import Point, Polygon
from typing import Dict, List, Any
from datetime import datetime, timezone

class SpatialGeofenceEngine:
    def __init__(self):
        self.geofences: Dict[str, Dict[str, Any]] = {}
        
        # Seed with a default restricted logistics terminal polygon (San Francisco Port Hub)
        default_coords = [
            (-122.4200, 37.7800),
            (-122.4000, 37.7800),
            (-122.4000, 37.8000),
            (-122.4200, 37.8000),
            (-122.4200, 37.7800)
        ]
        self.add_geofence("sf_hub_01", "San Francisco Logistics Port", default_coords)

    def add_geofence(self, zone_id: str, name: str, coords: List[tuple]) -> bool:
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        poly = Polygon(coords)
        self.geofences[zone_id] = {
            "name": name,
            "polygon": poly,
            "raw_coords": coords
        }
        return True

    def evaluate_containment(self, asset_id: str, lng: float, lat: float) -> Dict[str, Any]:
        point = Point(lng, lat)
        breached = []
        
        for zone_id, zone_data in self.geofences.items():
            if zone_data["polygon"].contains(point):
                breached.append(zone_data["name"])

        inside = len(breached) > 0
        alert = "RESTRICTED PERIMETER INTRUSION DETECTED" if inside else "AUTHORIZED / OUTSIDE GEOFENCE"
        
        return {
            "asset_id": asset_id,
            "latitude": lat,
            "longitude": lng,
            "inside_geofence": inside,
            "active_zones": breached,
            "alert_status": alert,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

spatial_engine = SpatialGeofenceEngine()
