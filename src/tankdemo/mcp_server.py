"""Read-only MCP server for the synthetic tank telemetry demo.

Run:
    python -m tankdemo.mcp_server

This server intentionally exposes read-only tools. Write actions such as moving tanks,
editing users, creating delivery orders, changing alarm thresholds, or acknowledging alerts
are excluded from the demo and would require explicit scopes, audit logs, and human approval.
"""

from __future__ import annotations

from . import data
from .risk import (
    explain_priority,
    monitor_health,
    portal_summary,
    runout_risk,
    tank_diagnostics,
    tank_status,
)

try:
    from mcp.server.fastmcp import FastMCP
except Exception as exc:  # pragma: no cover - helpful local error
    raise RuntimeError(
        "The MCP extra is required. Install with: pip install -e '.[mcp]'"
    ) from exc

mcp = FastMCP("industrial-tank-telemetry-agent-demo")


@mcp.tool()
def get_portal_summary() -> dict:
    """Return synthetic portal-style counts for tanks, alarms, comm status, and runout risk."""
    return portal_summary(data.tanks(), data.alerts())


@mcp.tool()
def get_field_catalog() -> dict:
    """Return synthetic selected/available column names for API surface mapping."""
    return data.field_catalog()


@mcp.tool()
def list_tanks(region: str | None = None, location_id: str | None = None) -> list[dict]:
    """List synthetic tanks, optionally filtered by region or location."""
    tanks = data.tanks()
    if region:
        tanks = [tank for tank in tanks if tank["region"].lower() == region.lower()]
    if location_id:
        tanks = [tank for tank in tanks if tank["location_id"].upper() == location_id.upper()]
    return tanks


@mcp.tool()
def search_tanks(query: str) -> list[dict]:
    """Search synthetic tanks by tank name, location, product, city, state, or serial/RTU ID."""
    needle = query.lower()
    return [
        tank for tank in data.tanks()
        if needle in tank["tank_name"].lower()
        or needle in tank["location_name"].lower()
        or needle in tank["product"].lower()
        or needle in tank["city"].lower()
        or needle in tank["state"].lower()
        or needle in tank["device"]["serial_rtu_id"].lower()
    ]


@mcp.tool()
def get_tank_status(tank_id: str) -> dict:
    """Return synthetic inventory, alarm, communication, sensor, and risk status for one tank."""
    tank = data.get_tank(tank_id)
    if not tank:
        return {"error": "tank_not_found", "tank_id": tank_id}
    return tank_status(tank)


@mcp.tool()
def get_tank_detail(tank_id: str) -> dict:
    """Return field-rich synthetic detail for one tank: inventory, device, alarm, schedule, and recent activity."""
    tank = data.get_tank(tank_id)
    if not tank:
        return {"error": "tank_not_found", "tank_id": tank_id}
    return {
        "tank": tank,
        "status": tank_status(tank),
        "diagnostics": tank_diagnostics(tank),
        "alerts": data.tank_alerts(tank_id),
        "readings": data.tank_readings(tank_id),
    }


@mcp.tool()
def get_tank_diagnostics(tank_id: str) -> dict:
    """Return synthetic device/RTU diagnostic information for one tank."""
    tank = data.get_tank(tank_id)
    if not tank:
        return {"error": "tank_not_found", "tank_id": tank_id}
    return tank_diagnostics(tank)


@mcp.tool()
def get_alarm_config(tank_id: str) -> dict:
    """Return synthetic alarm thresholds such as low, high, critical low, and temperature thresholds."""
    tank = data.get_tank(tank_id)
    if not tank:
        return {"error": "tank_not_found", "tank_id": tank_id}
    return {"tank_id": tank_id.upper(), **tank["alarms"]}


@mcp.tool()
def get_call_schedule(tank_id: str) -> dict:
    """Return synthetic call-out interval, call window, call days, and call-on-inventory setting."""
    tank = data.get_tank(tank_id)
    if not tank:
        return {"error": "tank_not_found", "tank_id": tank_id}
    return {"tank_id": tank_id.upper(), **tank["call_schedule"]}


@mcp.tool()
def explain_delivery_priority(tank_id: str) -> dict:
    """Explain why a tank should or should not be reviewed for dispatch."""
    tank = data.get_tank(tank_id)
    if not tank:
        return {"error": "tank_not_found", "tank_id": tank_id}
    return explain_priority(tank)


@mcp.tool()
def list_runout_risks(days: int = 7) -> list[dict]:
    """List tanks projected to hit empty/limit thresholds within the requested synthetic risk window."""
    return runout_risk(data.tanks(), days=days)


@mcp.tool()
def list_recent_alerts(severity: str | None = None) -> list[dict]:
    """List synthetic alerts, optionally filtered by severity."""
    rows = data.alerts()
    if severity:
        rows = [row for row in rows if row["severity"].lower() == severity.lower()]
    return rows


@mcp.tool()
def summarize_monitor_health() -> list[dict]:
    """Summarize synthetic monitor battery, RSSI, call, communication, and sensor health."""
    return monitor_health(data.tanks())


@mcp.tool()
def list_locations() -> list[dict]:
    """List synthetic locations and delivery forecasting parameters."""
    return data.locations()


@mcp.resource("tankdemo://policy/agent-safety")
def agent_safety_policy() -> str:
    """Return the demo's read-only agent access policy."""
    return (
        "This synthetic MCP server is read-only. It exposes summaries, tanks, locations, readings, "
        "alerts, alarm configuration, diagnostics, runout risk, and monitor health. It does not move "
        "tanks, edit users, change thresholds, create delivery orders, send notifications, acknowledge "
        "alerts, or dispatch drivers. Those actions would require explicit scopes, audit logging, and "
        "human approval."
    )


if __name__ == "__main__":
    mcp.run()
