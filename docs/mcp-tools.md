# MCP Tools

The MCP server exposes read-only tools for governed agent workflows.

The tool outputs come from synthetic fixtures only. The demo does not expose real customers, street addresses, users, emails, phone numbers, proprietary records, screenshots, logos, or real device IDs.

## Tools

- `get_portal_summary` — counts by alarm, comm status, sensor status, and runout risk.
- `get_field_catalog` — selected/available field catalog.
- `list_tanks` — list synthetic tanks.
- `search_tanks` — search synthetic tanks by name, location, product, city, state, or serial/RTU ID.
- `get_tank_status` — summarize one tank.
- `get_tank_detail` — full detail view for one tank.
- `get_tank_diagnostics` — RTU/sensor diagnostics.
- `get_alarm_config` — alarm thresholds.
- `get_call_schedule` — call interval/window/days.
- `explain_delivery_priority` — explain dispatch/human-review priority.
- `list_runout_risks` — list tanks needing review.
- `list_recent_alerts` — alerts filtered by severity.
- `summarize_monitor_health` — comm/sensor/battery/RSSI issue summary.
- `list_locations` — synthetic locations and delivery forecasting settings.

## Agent-safe examples

- “Which tanks are in critical low alarm and why?”
- “Summarize monitors with communication or sensor problems.”
- “Show tanks projected to hit empty/limit threshold within 7 days.”
- “What alarm thresholds are configured for TK-101?”
- “Which locations have multiple tanks and high dispatch priority?”

## Excluded write actions

Agents cannot move tanks, edit thresholds, edit users, acknowledge alarms, notify customers, or create delivery orders in this demo.
