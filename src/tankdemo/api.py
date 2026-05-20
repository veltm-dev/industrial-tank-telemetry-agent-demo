from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query

from . import data
from .risk import (
    explain_priority,
    monitor_health,
    portal_summary,
    runout_risk,
    tank_diagnostics,
    tank_status,
)

app = FastAPI(
    title="Industrial Tank Telemetry Agent Demo API",
    version="0.2.0",
    description=(
        "Synthetic, read-only API demonstrating field-aware API/CLI/MCP surfaces for tank "
        "telemetry, portal summaries, locations, alarm thresholds, diagnostics, dispatch risk, "
        "and monitor health. The fixtures intentionally omit customer records, street addresses, "
        "users, phone numbers, emails, screenshots, logos, proprietary records, and real device IDs."
    ),
)


@app.get("/")
def root() -> dict:
    return {
        "name": "Industrial Tank Telemetry Agent Demo",
        "synthetic_data_only": True,
        "read_only": True,
        "surfaces": ["REST API", "CLI", "MCP", "webhook model", "agent policy"],
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/summary")
def summary() -> dict:
    """Portal-style counts for alarms, tank status, comm status, and sensor health."""
    return portal_summary(data.tanks(), data.alerts())


@app.get("/field-catalog")
def field_catalog() -> dict:
    """Column/field catalog for API design and export/backward-compatibility discussion."""
    return data.field_catalog()


@app.get("/organizations")
def organizations() -> list[dict]:
    return data.organizations()


@app.get("/locations")
def locations(active_only: bool = True) -> list[dict]:
    rows = data.locations()
    if active_only:
        rows = [row for row in rows if row.get("active")]
    return rows


@app.get("/locations/{location_id}")
def get_location(location_id: str) -> dict:
    location = data.get_location(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return {**location, "tanks": data.location_tanks(location_id)}


@app.get("/tanks")
def list_tanks(
    region: str | None = None,
    location_id: str | None = None,
    status: str | None = Query(default=None, description="Filter by tank_status, e.g. OK or Inactive."),
) -> list[dict]:
    tanks = data.tanks()
    if region:
        tanks = [tank for tank in tanks if tank["region"].lower() == region.lower()]
    if location_id:
        tanks = [tank for tank in tanks if tank["location_id"].upper() == location_id.upper()]
    if status:
        tanks = [tank for tank in tanks if tank.get("status", {}).get("tank_status", "").lower() == status.lower()]
    return tanks


@app.get("/tanks/{tank_id}")
def get_tank(tank_id: str) -> dict:
    tank = data.get_tank(tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return tank


@app.get("/tanks/{tank_id}/status")
def get_tank_status(tank_id: str) -> dict:
    tank = data.get_tank(tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return tank_status(tank)


@app.get("/tanks/{tank_id}/detail")
def get_tank_detail(tank_id: str) -> dict:
    """Field-rich detail view: inventory, status, device, diagnostics, alarms, and schedule."""
    tank = data.get_tank(tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return {
        "tank": tank,
        "status": tank_status(tank),
        "diagnostics": tank_diagnostics(tank),
        "recent_alerts": data.tank_alerts(tank_id),
        "recent_readings": data.tank_readings(tank_id),
    }


@app.get("/tanks/{tank_id}/explain")
def explain_tank_priority(tank_id: str) -> dict:
    tank = data.get_tank(tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return explain_priority(tank)


@app.get("/tanks/{tank_id}/diagnostics")
def get_tank_diagnostics(tank_id: str) -> dict:
    tank = data.get_tank(tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return tank_diagnostics(tank)


@app.get("/tanks/{tank_id}/alarm-config")
def get_alarm_config(tank_id: str) -> dict:
    tank = data.get_tank(tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return {"tank_id": tank_id.upper(), **tank["alarms"]}


@app.get("/tanks/{tank_id}/call-schedule")
def get_call_schedule(tank_id: str) -> dict:
    tank = data.get_tank(tank_id)
    if not tank:
        raise HTTPException(status_code=404, detail="Tank not found")
    return {"tank_id": tank_id.upper(), **tank["call_schedule"]}


@app.get("/readings")
def list_readings(tank_id: str | None = None) -> list[dict]:
    if tank_id:
        return data.tank_readings(tank_id)
    return data.readings()


@app.get("/alerts")
def list_alerts(
    severity: str | None = Query(default=None, description="critical, warning, info"),
    tank_id: str | None = None,
) -> list[dict]:
    alerts = data.alerts()
    if severity:
        alerts = [alert for alert in alerts if alert["severity"].lower() == severity.lower()]
    if tank_id:
        alerts = [alert for alert in alerts if alert["tank_id"].upper() == tank_id.upper()]
    return alerts


@app.get("/runout-risk")
def list_runout_risk(days: int = Query(default=7, ge=1, le=30)) -> list[dict]:
    return runout_risk(data.tanks(), days=days)


@app.get("/monitor-health")
def list_monitor_health() -> list[dict]:
    return monitor_health(data.tanks())


@app.get("/map-points")
def map_points() -> list[dict]:
    return [
        {
            "tank_id": tank["id"],
            "tank_name": tank["tank_name"],
            "location_name": tank["location_name"],
            "lat": tank["location"]["lat"],
            "lon": tank["location"]["lon"],
            "map_note": "Synthetic map coordinate; not a customer or field site.",
            "risk_level": tank_status(tank)["risk_level"],
            "volume_alarm_status": tank.get("status", {}).get("volume_alarm_status"),
        }
        for tank in data.tanks()
    ]


@app.get("/webhook-events")
def webhook_events() -> list[dict]:
    return [
        {"event": "tank.inventory.updated", "description": "New net/gross inventory reading received."},
        {"event": "tank.volume_alarm.changed", "description": "Volume alarm status changes, e.g. OK to Critical Low Alarm."},
        {"event": "tank.runout_risk", "description": "Projected empty/limit window enters configured threshold."},
        {"event": "tank.delivery.detected", "description": "Inventory jump suggests a delivery event."},
        {"event": "tank.short_fill.detected", "description": "Detected fill is below configured short-fill amount."},
        {"event": "monitor.comm_status.changed", "description": "Comm status changes or device stops reporting."},
        {"event": "monitor.sensor_status.changed", "description": "Sensor status changes."},
        {"event": "monitor.low_battery", "description": "Battery drops below configured threshold."},
        {"event": "location.forecast.updated", "description": "Delivery forecasting parameter changes."},
    ]


@app.get("/agent-policy")
def agent_policy() -> dict:
    return {
        "default_mode": "read_only",
        "write_actions": "disabled_in_demo",
        "human_review_required_for": [
            "move_tanks",
            "dispatch_changes",
            "customer_notifications",
            "delivery_orders",
            "acknowledge_alerts",
            "edit_alarm_thresholds",
            "edit_users_or_permissions",
        ],
        "example_scopes": [
            "summary:read",
            "tanks:read",
            "locations:read",
            "alerts:read",
            "readings:read",
            "diagnostics:read",
            "risk:read",
            "monitor_health:read",
        ],
        "audit_log_required": True,
        "synthetic_data_only": True,
    }
