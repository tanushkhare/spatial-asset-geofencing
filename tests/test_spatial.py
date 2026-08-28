import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "healthy"

def test_point_inside_geofence():
    # Inside the default SF Logistics Hub (-122.41, 37.79)
    payload = {"asset_id": "TEST_ASSET_IN", "longitude": -122.4100, "latitude": 37.7900}
    res = client.post("/api/v1/spatial/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["inside_geofence"] is True
    assert "San Francisco Logistics Port" in data["active_zones"]

def test_point_outside_geofence():
    # Outside the hub (e.g. New York coordinates)
    payload = {"asset_id": "TEST_ASSET_OUT", "longitude": -74.0060, "latitude": 40.7128}
    res = client.post("/api/v1/spatial/evaluate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["inside_geofence"] is False
    assert len(data["active_zones"]) == 0
