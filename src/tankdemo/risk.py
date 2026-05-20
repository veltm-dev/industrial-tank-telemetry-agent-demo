from __future__ import annotations

from collections import Counter
from typing import Any


def current_gallons(tank: dict[str, Any]) -> float:
    return float(tank.get("inventory_gross_gal") or tank.get("current_gal") or 0)


def capacity_gallons(tank: dict[str, Any]) -> float:
    return float(tank.get("capacity_limit_gal") or tank.get("capacity_gal") or 0)


def battery_pct(tank: dict[str, Any]) -> float:
    return float(tank.get("device", {}).get("battery_pct", tank.get("battery_pct", 0)))


def comm_status(tank: dict[str, Any]) -> str:
    return str(tank.get("status", {}).get("comm_status", tank.get("monitor_status", "unknown")))


def sensor_status(tank: dict[str, Any]) -> str:
    return str(tank.get("status", {}).get("sensor_status", "unknown"))


def volume_alarm_status(tank: dict[str, Any]) -> str:
    return str(tank.get("status", {}).get("volume_alarm_status", "OK"))


def days_until_empty(tank: dict[str, Any]) -> float | None:
    if isinstance(tank.get("days_to_limit_empty"), (int, float)):
        return round(float(tank["days_to_limit_empty"]), 2)
    usage = float(tank.get("daily_usage_gal") or 0)
    gallons = current_gallons(tank)
    if usage <= 0:
        return None
    return round(gallons / usage, 2)


def fill_pct(tank: dict[str, Any]) -> float:
    if isinstance(tank.get("volume_pct"), (int, float)):
        return round(float(tank["volume_pct"]), 1)
    capacity = capacity_gallons(tank)
    gallons = current_gallons(tank)
    if capacity <= 0:
        return 0.0
    return round((gallons / capacity) * 100, 1)


def risk_level(tank: dict[str, Any]) -> str:
    days = days_until_empty(tank)
    alarm = volume_alarm_status(tank).lower()
    comm = comm_status(tank).lower()
    sensor = sensor_status(tank).lower()

    if "critical" in alarm:
        return "critical"
    if days is not None and days <= 3:
        return "critical"
    if comm != "ok" and fill_pct(tank) < 25:
        return "critical"
    if "high alarm" in alarm or days is not None and days <= 7:
        return "high"
    if battery_pct(tank) < 30 or comm != "ok" or sensor != "ok":
        return "watch"
    return "normal"


def tank_status(tank: dict[str, Any]) -> dict[str, Any]:
    days = days_until_empty(tank)
    device = tank.get("device", {})
    status = tank.get("status", {})
    return {
        "tank_id": tank["id"],
        "tank_name": tank["tank_name"],
        "organization": tank["organization"],
        "location_name": tank["location_name"],
        "city": tank["city"],
        "state": tank["state"],
        "region": tank["region"],
        "route": tank.get("route", ""),
        "product": tank["product"],
        "inventory_time": tank["inventory_time"],
        "inventory_gross_gal": tank["inventory_gross_gal"],
        "inventory_net_gal": tank["inventory_net_gal"],
        "capacity_gal": tank["capacity_gal"],
        "available_capacity_gal": tank["available_capacity_gal"],
        "level_in": tank["level_in"],
        "fill_pct": fill_pct(tank),
        "empty_pct": tank.get("empty_pct"),
        "daily_usage_gal": tank["daily_usage_gal"],
        "avg_daily_usage_7": tank.get("avg_daily_usage_7"),
        "avg_daily_usage_35": tank.get("avg_daily_usage_35"),
        "days_until_empty": days,
        "days_to_alarm": tank.get("days_to_alarm"),
        "days_to_critical": tank.get("days_to_critical"),
        "days_to_reorder": tank.get("days_to_reorder"),
        "days_to_safety_stock": tank.get("days_to_safety_stock"),
        "risk_level": risk_level(tank),
        "volume_alarm_status": status.get("volume_alarm_status"),
        "comm_status": status.get("comm_status"),
        "sensor_status": status.get("sensor_status"),
        "maintenance_status": status.get("maintenance_status"),
        "tank_status": status.get("tank_status"),
        "battery_pct": device.get("battery_pct"),
        "rssi": device.get("rssi"),
        "temperature_f": device.get("temperature_f"),
        "serial_rtu_id": device.get("serial_rtu_id"),
    }


def explain_priority(tank: dict[str, Any]) -> dict[str, Any]:
    status = tank_status(tank)
    reasons: list[str] = []
    recommended_action = "No immediate action required."

    if status["risk_level"] == "critical":
        recommended_action = "Escalate for dispatch or human review today."
    elif status["risk_level"] == "high":
        recommended_action = "Place on delivery planning board for this week."
    elif status["risk_level"] == "watch":
        recommended_action = "Review monitor health and schedule service if needed."

    if status["volume_alarm_status"] and status["volume_alarm_status"] != "OK":
        reasons.append(f"Volume alarm status is {status['volume_alarm_status']}.")
    if status["days_until_empty"] is not None and status["days_until_empty"] <= 7:
        reasons.append(
            f"Projected empty/limit window is {status['days_until_empty']} days based on "
            f"{status['daily_usage_gal']} gal/day synthetic usage."
        )
    if status["fill_pct"] < 25:
        reasons.append(f"Inventory is {status['fill_pct']}% of capacity.")
    if status["comm_status"] != "OK":
        reasons.append(f"Communication status is {status['comm_status']}.")
    if status["sensor_status"] != "OK":
        reasons.append(f"Sensor status is {status['sensor_status']}.")
    if (status["battery_pct"] or 100) < 30:
        reasons.append(f"Battery is low at {status['battery_pct']}%.")
    if not reasons:
        reasons.append("Inventory, alarm, usage, communication, and sensor health are normal in the synthetic data.")

    return {
        **status,
        "reasons": reasons,
        "recommended_action": recommended_action,
        "human_review_required": status["risk_level"] in {"critical", "high"},
    }


def runout_risk(tanks: list[dict[str, Any]], days: int = 7) -> list[dict[str, Any]]:
    results = []
    for tank in tanks:
        status = tank_status(tank)
        due = status["days_until_empty"] is not None and status["days_until_empty"] <= days
        alarm_due = str(status.get("volume_alarm_status", "")).lower() in {
            "critical low alarm",
            "low alarm",
        }
        stale_low = status["comm_status"] != "OK" and status["fill_pct"] < 25
        if due or alarm_due or stale_low:
            results.append(explain_priority(tank))
    return sorted(results, key=lambda row: (row["days_until_empty"] is None, row["days_until_empty"] or 999))


def monitor_health(tanks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for tank in tanks:
        status = tank.get("status", {})
        device = tank.get("device", {})
        issue_count = 0
        issues: list[str] = []
        if status.get("comm_status") != "OK":
            issue_count += 1
            issues.append(f"comm={status.get('comm_status')}")
        if status.get("sensor_status") != "OK":
            issue_count += 1
            issues.append(f"sensor={status.get('sensor_status')}")
        if device.get("battery_pct", 100) < 30:
            issue_count += 1
            issues.append(f"battery={device.get('battery_pct')}%")
        if device.get("rssi") in {None, 0} or device.get("rssi", 100) < 35:
            issue_count += 1
            issues.append(f"rssi={device.get('rssi')}")
        if device.get("failed_calls", 0) > 0:
            issue_count += 1
            issues.append(f"failed_calls={device.get('failed_calls')}")
        rows.append(
            {
                "tank_id": tank["id"],
                "tank_name": tank["tank_name"],
                "location_name": tank["location_name"],
                "comm_status": status.get("comm_status"),
                "sensor_status": status.get("sensor_status"),
                "battery_pct": device.get("battery_pct"),
                "rssi": device.get("rssi"),
                "failed_calls": device.get("failed_calls"),
                "issue_count": issue_count,
                "issues": issues,
            }
        )
    return sorted(rows, key=lambda row: row["issue_count"], reverse=True)


def portal_summary(tanks: list[dict[str, Any]], alerts: list[dict[str, Any]]) -> dict[str, Any]:
    tank_status_counts = Counter(tank.get("status", {}).get("tank_status", "Unknown") for tank in tanks)
    alarm_counts = Counter(tank.get("status", {}).get("volume_alarm_status", "Unknown") for tank in tanks)
    comm_counts = Counter(tank.get("status", {}).get("comm_status", "Unknown") for tank in tanks)
    sensor_counts = Counter(tank.get("status", {}).get("sensor_status", "Unknown") for tank in tanks)
    return {
        "active_tanks": sum(1 for tank in tanks if tank.get("status", {}).get("tank_status") != "Inactive"),
        "inactive_tanks": sum(1 for tank in tanks if tank.get("status", {}).get("tank_status") == "Inactive"),
        "total_tanks": len(tanks),
        "open_alerts": sum(1 for alert in alerts if not alert.get("acknowledged")),
        "tank_status_counts": dict(tank_status_counts),
        "volume_alarm_counts": dict(alarm_counts),
        "comm_status_counts": dict(comm_counts),
        "sensor_status_counts": dict(sensor_counts),
        "runout_risk_count": len(runout_risk(tanks, days=7)),
    }


def tank_diagnostics(tank: dict[str, Any]) -> dict[str, Any]:
    device = tank.get("device", {})
    return {
        "tank_id": tank["id"],
        "rtu_model_number": device.get("rtu_model_number"),
        "rtu_model_type": device.get("rtu_model_type"),
        "firmware_version": device.get("firmware_version"),
        "sensor_type": device.get("sensor_type"),
        "temperature_f": device.get("temperature_f"),
        "level_numerator": device.get("level_numerator"),
        "level_denominator": device.get("level_denominator"),
        "rssi": device.get("rssi"),
        "rssi_min": device.get("rssi_min"),
        "rssi_max": device.get("rssi_max"),
        "total_calls": device.get("total_calls"),
        "reported_calls": device.get("reported_calls"),
        "failed_calls": device.get("failed_calls"),
        "transmit_sequence": device.get("transmit_sequence"),
        "acknowledged_sequence": device.get("acknowledged_sequence"),
        "carrier": device.get("carrier"),
        "download_status": device.get("download_status"),
        "call_out": device.get("call_out"),
    }
