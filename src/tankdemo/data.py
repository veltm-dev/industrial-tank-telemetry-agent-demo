from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"


def _load(name: str) -> list[dict[str, Any]] | dict[str, Any]:
    path = DATA_DIR / name
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def tanks() -> list[dict[str, Any]]:
    return _load("tanks.json")  # type: ignore[return-value]


@lru_cache(maxsize=1)
def alerts() -> list[dict[str, Any]]:
    return _load("alerts.json")  # type: ignore[return-value]


@lru_cache(maxsize=1)
def readings() -> list[dict[str, Any]]:
    return _load("readings.json")  # type: ignore[return-value]


@lru_cache(maxsize=1)
def locations() -> list[dict[str, Any]]:
    return _load("locations.json")  # type: ignore[return-value]


@lru_cache(maxsize=1)
def organizations() -> list[dict[str, Any]]:
    return _load("organizations.json")  # type: ignore[return-value]


@lru_cache(maxsize=1)
def field_catalog() -> dict[str, Any]:
    return _load("field_catalog.json")  # type: ignore[return-value]


def get_tank(tank_id: str) -> dict[str, Any] | None:
    tank_id = tank_id.upper()
    return next((tank for tank in tanks() if tank["id"].upper() == tank_id), None)


def tank_alerts(tank_id: str) -> list[dict[str, Any]]:
    tank_id = tank_id.upper()
    return [alert for alert in alerts() if alert["tank_id"].upper() == tank_id]


def tank_readings(tank_id: str) -> list[dict[str, Any]]:
    tank_id = tank_id.upper()
    return [reading for reading in readings() if reading["tank_id"].upper() == tank_id]


def get_location(location_id: str) -> dict[str, Any] | None:
    location_id = location_id.upper()
    return next((location for location in locations() if location["id"].upper() == location_id), None)


def get_organization(organization_id: str) -> dict[str, Any] | None:
    organization_id = organization_id.upper()
    return next((org for org in organizations() if org["id"].upper() == organization_id), None)


def location_tanks(location_id: str) -> list[dict[str, Any]]:
    location_id = location_id.upper()
    return [tank for tank in tanks() if tank["location_id"].upper() == location_id]
