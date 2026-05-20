from fastapi.testclient import TestClient

from tankdemo.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_summary():
    response = client.get("/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["total_tanks"] >= 8
    assert payload["runout_risk_count"] >= 1


def test_field_catalog():
    response = client.get("/field-catalog")
    assert response.status_code == 200
    payload = response.json()
    assert "Volume Alarm Status" in payload["selected_columns"]
    assert "RSSI" in payload["available_columns"]


def test_get_tank_status():
    response = client.get("/tanks/TK-101/status")
    assert response.status_code == 200
    payload = response.json()
    assert payload["tank_id"] == "TK-101"
    assert payload["risk_level"] == "critical"
    assert payload["volume_alarm_status"] == "Critical Low Alarm"


def test_tank_diagnostics():
    response = client.get("/tanks/TK-101/diagnostics")
    assert response.status_code == 200
    payload = response.json()
    assert payload["rtu_model_number"]
    assert payload["rssi"] == 62


def test_runout_risk():
    response = client.get("/runout-risk?days=7")
    assert response.status_code == 200
    ids = {row["tank_id"] for row in response.json()}
    assert "TK-101" in ids
    assert "TK-105" in ids


def test_required_read_only_endpoints_are_available():
    endpoints = [
        "/summary",
        "/field-catalog",
        "/organizations",
        "/locations",
        "/locations/LOC-101",
        "/tanks",
        "/tanks/TK-101",
        "/tanks/TK-101/status",
        "/tanks/TK-101/detail",
        "/tanks/TK-101/explain",
        "/tanks/TK-101/diagnostics",
        "/tanks/TK-101/alarm-config",
        "/tanks/TK-101/call-schedule",
        "/readings",
        "/alerts",
        "/runout-risk?days=7",
        "/monitor-health",
        "/map-points",
        "/webhook-events",
        "/agent-policy",
    ]

    for endpoint in endpoints:
        response = client.get(endpoint)
        assert response.status_code == 200, endpoint


def test_agent_policy_is_read_only():
    response = client.get("/agent-policy")
    assert response.status_code == 200
    payload = response.json()
    assert payload["default_mode"] == "read_only"
    assert payload["write_actions"] == "disabled_in_demo"
    assert payload["synthetic_data_only"] is True


def test_map_points_are_marked_synthetic():
    response = client.get("/map-points")
    assert response.status_code == 200
    payload = response.json()
    assert payload
    assert all("Synthetic map coordinate" in point["map_note"] for point in payload)
