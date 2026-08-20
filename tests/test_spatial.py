import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_geofence_containment_breach():
    # Inside the default SF terminal polygon
    payload = {"asset_id": "TEST_VEHICLE_1", "longitude": -122.4100, "latitude": 37.7900, "speed_kmh": 30.0}
    res = client.post("/api/v1/spatial/telemetry", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["inside_geofence"] is True
    assert len(data["active_zones"]) > 0

def test_geofence_outside_boundary():
    # Far outside SF zone
    payload = {"asset_id": "TEST_VEHICLE_2", "longitude": -121.0000, "latitude": 36.0000, "speed_kmh": 65.0}
    res = client.post("/api/v1/spatial/telemetry", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["inside_geofence"] is False
    assert len(data["active_zones"]) == 0
