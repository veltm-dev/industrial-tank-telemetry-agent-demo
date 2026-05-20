# API Spec Summary

This is a same-day proof-of-concept API, not a production API contract. It is read-only and uses synthetic data only.

## Primary endpoints

- `GET /summary` — portal-style counts for tanks, alarms, comm status, sensor status, and runout risk.
- `GET /field-catalog` — selected and available fields for column/export/API mapping.
- `GET /organizations` — synthetic organizations.
- `GET /locations` — synthetic locations with delivery forecasting parameters. Street addresses are intentionally omitted.
- `GET /locations/{location_id}` — one location plus its tanks.
- `GET /tanks` — field-rich synthetic tank list.
- `GET /tanks/{tank_id}/detail` — detail view: inventory, device, diagnostics, alarms, schedule, readings, alerts.
- `GET /tanks/{tank_id}/status` — summarized status and risk.
- `GET /tanks/{tank_id}/diagnostics` — RTU/sensor/call diagnostic values.
- `GET /tanks/{tank_id}/alarm-config` — threshold configuration.
- `GET /tanks/{tank_id}/call-schedule` — call window, interval, days, call-on-inventory.
- `GET /readings` — synthetic inventory history.
- `GET /alerts` — synthetic alarms/alerts.
- `GET /runout-risk` — tanks that need dispatch/human review.
- `GET /monitor-health` — comm/sensor/battery/RSSI issues.
- `GET /map-points` — map-ready tank points with alarm/risk status.
- `GET /webhook-events` — event types for integrations.
- `GET /agent-policy` — read-only access policy and write-action boundaries.

## Design note

The API is intentionally read-only. The goal is to demonstrate a safe platform surface that could sit beside an existing portal without forcing a rip-and-replace.
