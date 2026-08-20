from shapely.geometry import Point, Polygon
from typing import Dict, List, Any
from datetime import datetime, timezone

class SpatialGeofenceEngine:
    def __init__(self):
        # In-memory spatial index of active polygons
        self.geofences: Dict[str, Dict[str, Any]] = {}
        
        # Bootstrap with a default logistics terminal zone (San Francisco Port Corridor)
        default_poly = [
            (-122.42, 37.78),
            (-122.40, 37.78),
            (-122.40, 37.80),
            (-122.42, 37.80),
            (-122.42, 37.78)
        ]
        self.add_geofence("sf_port_terminal", "San Francisco Logistics Hub", default_poly)

    def add_geofence(self, zone_id: str, name: str, coords: List[tuple]) -> bool:
        # Shapely requires closed polygon ring
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        polygon = Polygon(coords)
        self.geofences[zone_id] = {
            "name": name,
            "polygon": polygon,
            "raw_coords": coords
        }
        return True

    def check_point_containment(self, asset_id: str, lng: float, lat: float) -> Dict[str, Any]:
        point = Point(lng, lat)
        breached_zones = []
        
        for zone_id, zone_data in self.geofences.items():
            if zone_data["polygon"].contains(point):
                breached_zones.append(zone_data["name"])
        
        inside = len(breached_zones) > 0
        alert = "SECURITY BREACH: INSIDE RESTRICTED PERIMETER" if inside else "AUTHORIZED: OUTSIDE GEOFENCE BOUNDARY"
        
        return {
            "asset_id": asset_id,
            "latitude": lat,
            "longitude": lng,
            "inside_geofence": inside,
            "active_zones": breached_zones,
            "alert_status": alert,
            "timestamp": datetime.now(timezone.utc)
        }

spatial_engine = SpatialGeofenceEngine()
