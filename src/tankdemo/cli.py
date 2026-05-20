from __future__ import annotations

import json
from typing import Any

import typer
from rich.console import Console
from rich.table import Table

from . import data
from .risk import explain_priority, monitor_health, portal_summary, runout_risk, tank_diagnostics, tank_status

app = typer.Typer(help="Synthetic tank telemetry CLI for API/CLI/MCP concept demo.")
tanks_app = typer.Typer(help="Tank list and runout-risk commands.")
tank_app = typer.Typer(help="Single-tank inspection commands.")
alerts_app = typer.Typer(help="Alert commands.")
monitors_app = typer.Typer(help="Monitor health commands.")
locations_app = typer.Typer(help="Location commands.")
fields_app = typer.Typer(help="Portal-style field catalog commands.")
console = Console()


def _json(data_: Any) -> None:
    console.print_json(json.dumps(data_, indent=2))


@app.command("summary")
def summary(as_json: bool = False) -> None:
    payload = portal_summary(data.tanks(), data.alerts())
    if as_json:
        _json(payload)
        return
    table = Table(title="Synthetic Portal Summary")
    table.add_column("Metric")
    table.add_column("Value")
    for key in ["active_tanks", "inactive_tanks", "total_tanks", "open_alerts", "runout_risk_count"]:
        table.add_row(key, str(payload[key]))
    table.add_row("volume_alarm_counts", str(payload["volume_alarm_counts"]))
    table.add_row("comm_status_counts", str(payload["comm_status_counts"]))
    console.print(table)


@fields_app.command("list")
def list_fields(as_json: bool = False) -> None:
    payload = data.field_catalog()
    if as_json:
        _json(payload)
        return
    table = Table(title="Field Catalog")
    table.add_column("Selected Columns")
    table.add_column("Available Columns")
    selected = payload["selected_columns"]
    available = payload["available_columns"]
    max_len = max(len(selected), len(available))
    for i in range(max_len):
        table.add_row(selected[i] if i < len(selected) else "", available[i] if i < len(available) else "")
    console.print(table)


@locations_app.command("list")
def list_locations(as_json: bool = False) -> None:
    rows = data.locations()
    if as_json:
        _json(rows)
        return
    table = Table(title="Synthetic Locations")
    for col in ["ID", "Name", "City", "State", "Tanks", "Target Delivery %"]:
        table.add_column(col)
    for row in rows:
        table.add_row(row["id"], row["name"], row["city"], row["state"], str(row["number_of_tanks"]), str(row["target_delivery_pct"]))
    console.print(table)


@locations_app.command("show")
def show_location(location_id: str, as_json: bool = False) -> None:
    location = data.get_location(location_id)
    if not location:
        raise typer.BadParameter("Location not found")
    payload = {**location, "tanks": data.location_tanks(location_id)}
    if as_json:
        _json(payload)
        return
    table = Table(title=f"Location: {location['name']}")
    table.add_column("Field")
    table.add_column("Value")
    for key in ["id", "name", "city", "state", "timezone", "number_of_tanks", "target_delivery_pct", "average_delivery_cost"]:
        table.add_row(key, str(location.get(key)))
    console.print(table)


@tanks_app.command("list")
def list_tanks(
    region: str | None = typer.Option(None, help="Filter by region."),
    location_id: str | None = typer.Option(None, help="Filter by location ID."),
    as_json: bool = False,
) -> None:
    tanks = data.tanks()
    if region:
        tanks = [tank for tank in tanks if tank["region"].lower() == region.lower()]
    if location_id:
        tanks = [tank for tank in tanks if tank["location_id"].upper() == location_id.upper()]
    if as_json:
        _json(tanks)
        return
    table = Table(title="Synthetic Tanks")
    for col in ["ID", "Tank", "Location", "Product", "Net", "Gross", "Volume %", "Alarm", "Comm", "Sensor", "Battery"]:
        table.add_column(col)
    for tank in tanks:
        table.add_row(
            tank["id"],
            tank["tank_name"],
            tank["location_name"],
            tank["product"],
            str(tank["inventory_net_gal"]),
            str(tank["inventory_gross_gal"]),
            str(tank["volume_pct"]),
            tank["status"]["volume_alarm_status"],
            tank["status"]["comm_status"],
            tank["status"]["sensor_status"],
            str(tank["device"]["battery_pct"]),
        )
    console.print(table)


@tanks_app.command("at-risk")
def at_risk(days: int = typer.Option(7, help="Runout risk window in days."), as_json: bool = False) -> None:
    rows = runout_risk(data.tanks(), days=days)
    if as_json:
        _json(rows)
        return
    table = Table(title=f"Runout / Alarm Risk <= {days} days")
    for col in ["Tank", "Name", "Location", "Fill %", "Days", "Alarm", "Risk", "Action"]:
        table.add_column(col)
    for row in rows:
        table.add_row(
            row["tank_id"], row["tank_name"], row["location_name"], str(row["fill_pct"]),
            str(row["days_until_empty"]), str(row["volume_alarm_status"]), row["risk_level"], row["recommended_action"]
        )
    console.print(table)


@tank_app.command("status")
def status(tank_id: str, as_json: bool = False) -> None:
    tank = data.get_tank(tank_id)
    if not tank:
        raise typer.BadParameter("Tank not found")
    payload = tank_status(tank)
    if as_json:
        _json(payload)
        return
    table = Table(title=f"Tank Status: {payload['tank_id']}")
    table.add_column("Field")
    table.add_column("Value")
    for key, value in payload.items():
        table.add_row(key, str(value))
    console.print(table)


@tank_app.command("detail")
def detail(tank_id: str, as_json: bool = False) -> None:
    tank = data.get_tank(tank_id)
    if not tank:
        raise typer.BadParameter("Tank not found")
    payload = {"tank": tank, "status": tank_status(tank), "diagnostics": tank_diagnostics(tank), "alerts": data.tank_alerts(tank_id)}
    if as_json:
        _json(payload)
        return
    console.print(f"[bold]{tank['id']} — {tank['tank_name']} / {tank['location_name']}[/bold]")
    console.print(f"Product: {tank['product']} | Inventory: {tank['inventory_gross_gal']} gal gross | Volume: {tank['volume_pct']}%")
    console.print(f"Alarm: {tank['status']['volume_alarm_status']} | Comm: {tank['status']['comm_status']} | Sensor: {tank['status']['sensor_status']}")


@tank_app.command("explain")
def explain(tank_id: str, as_json: bool = False) -> None:
    tank = data.get_tank(tank_id)
    if not tank:
        raise typer.BadParameter("Tank not found")
    payload = explain_priority(tank)
    if as_json:
        _json(payload)
        return
    console.print(f"[bold]{payload['tank_id']} — {payload['tank_name']} / {payload['location_name']}[/bold]")
    console.print(f"Risk: {payload['risk_level']} | Action: {payload['recommended_action']}")
    console.print("Reasons:")
    for reason in payload["reasons"]:
        console.print(f"- {reason}")


@tank_app.command("diagnostics")
def diagnostics(tank_id: str, as_json: bool = False) -> None:
    tank = data.get_tank(tank_id)
    if not tank:
        raise typer.BadParameter("Tank not found")
    payload = tank_diagnostics(tank)
    if as_json:
        _json(payload)
        return
    table = Table(title=f"Diagnostics: {tank_id.upper()}")
    table.add_column("Field")
    table.add_column("Value")
    for key, value in payload.items():
        table.add_row(key, str(value))
    console.print(table)


@tank_app.command("alarms")
def alarms(tank_id: str, as_json: bool = False) -> None:
    tank = data.get_tank(tank_id)
    if not tank:
        raise typer.BadParameter("Tank not found")
    payload = {"tank_id": tank_id.upper(), **tank["alarms"]}
    if as_json:
        _json(payload)
        return
    table = Table(title=f"Alarm Config: {tank_id.upper()}")
    table.add_column("Field")
    table.add_column("Value")
    for key, value in payload.items():
        table.add_row(key, str(value))
    console.print(table)


@tank_app.command("schedule")
def schedule(tank_id: str, as_json: bool = False) -> None:
    tank = data.get_tank(tank_id)
    if not tank:
        raise typer.BadParameter("Tank not found")
    payload = {"tank_id": tank_id.upper(), **tank["call_schedule"]}
    if as_json:
        _json(payload)
        return
    table = Table(title=f"Call Schedule: {tank_id.upper()}")
    table.add_column("Field")
    table.add_column("Value")
    for key, value in payload.items():
        table.add_row(key, str(value))
    console.print(table)


@alerts_app.command("list")
def list_alerts(severity: str | None = None, tank_id: str | None = None, as_json: bool = False) -> None:
    rows = data.alerts()
    if severity:
        rows = [row for row in rows if row["severity"].lower() == severity.lower()]
    if tank_id:
        rows = [row for row in rows if row["tank_id"].upper() == tank_id.upper()]
    if as_json:
        _json(rows)
        return
    table = Table(title="Synthetic Alerts")
    for col in ["ID", "Tank", "Severity", "Type", "Message", "Ack"]:
        table.add_column(col)
    for row in rows:
        table.add_row(row["id"], row["tank_id"], row["severity"], row["type"], row["message"], str(row["acknowledged"]))
    console.print(table)


@monitors_app.command("health")
def health(as_json: bool = False) -> None:
    rows = monitor_health(data.tanks())
    if as_json:
        _json(rows)
        return
    table = Table(title="Monitor Health")
    for col in ["Tank", "Name", "Comm", "Sensor", "Battery", "RSSI", "Issues"]:
        table.add_column(col)
    for row in rows:
        table.add_row(row["tank_id"], row["tank_name"], row["comm_status"], row["sensor_status"], str(row["battery_pct"]), str(row["rssi"]), ", ".join(row["issues"]) or "none")
    console.print(table)


app.add_typer(fields_app, name="fields")
app.add_typer(locations_app, name="locations")
app.add_typer(tanks_app, name="tanks")
app.add_typer(tank_app, name="tank")
app.add_typer(alerts_app, name="alerts")
app.add_typer(monitors_app, name="monitors")

if __name__ == "__main__":
    app()
