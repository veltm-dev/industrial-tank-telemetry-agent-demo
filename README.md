# Industrial Tank Telemetry Agent Demo

A synthetic, non-proprietary proof of concept showing how an industrial tank telemetry platform could expose governed **API**, **CLI**, **webhook**, and **MCP** surfaces for dispatch, support, integrations, field operations, and agentic workflows.

> **Important:** This demo uses synthetic data only. It does not access AMETEK, Telular, SkyBitz, SmartTank, customer systems, customer records, proprietary portals, screenshots, logos, addresses, users, phone numbers, emails, or device records. It is not affiliated with or endorsed by those companies. The purpose is to demonstrate an inspectable product and architecture direction.

Live links:

- GitHub repo: <https://github.com/veltm-dev/industrial-tank-telemetry-agent-demo>
- Static landing page: <https://industrial-tank-telemetry-agent-dem.vercel.app>

## What This Demo Proves

This is a same-day credibility packet, not a production SaaS application. It proves that tank telemetry can become programmable without replacing the existing portal:

- A field-aware REST API can expose summaries, organizations, locations, tanks, readings, alerts, diagnostics, alarm thresholds, call schedules, map points, webhook events, runout risk, and agent policy.
- A CLI can give support, product, field operations, and integration teams repeatable inspection workflows.
- A read-only MCP server can let agents answer operational questions without granting broad UI access or unsafe write permissions.
- Governance can be explicit from day one: read-only defaults, scoped writes, audit logging, and human approval for operational changes.

## Fast start

```bash
git clone https://github.com/veltm-dev/industrial-tank-telemetry-agent-demo.git
cd industrial-tank-telemetry-agent-demo
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev,mcp]'
python -m uvicorn tankdemo.api:app --reload
```

Open API docs:

```text
http://localhost:8000/docs
```

Run CLI commands:

```bash
source .venv/bin/activate
tankctl summary
tankctl fields list
tankctl locations list
tankctl tanks list
tankctl tanks at-risk --days 7
tankctl tank status TK-101
tankctl tank detail TK-101
tankctl tank diagnostics TK-101
tankctl tank alarms TK-101
tankctl tank schedule TK-101
tankctl tank explain TK-101
tankctl alerts list --severity critical
tankctl monitors health
```

Run the static landing page locally by opening:

```text
site/index.html
```

Run tests:

```bash
source .venv/bin/activate
python -m pytest
```

Run the MCP server over stdio:

```bash
python -m tankdemo.mcp_server
```

## API examples

```bash
curl http://localhost:8000/summary
curl http://localhost:8000/field-catalog
curl http://localhost:8000/locations
curl http://localhost:8000/tanks
curl http://localhost:8000/tanks/TK-101/detail
curl http://localhost:8000/tanks/TK-101/diagnostics
curl http://localhost:8000/tanks/TK-101/alarm-config
curl http://localhost:8000/tanks/TK-101/call-schedule
curl 'http://localhost:8000/runout-risk?days=7'
curl 'http://localhost:8000/alerts?severity=critical'
curl http://localhost:8000/monitor-health
curl http://localhost:8000/map-points
curl http://localhost:8000/webhook-events
curl http://localhost:8000/agent-policy
```

## CLI Surface

The CLI is intentionally read-only and optimized for inspection:

- `tankctl summary`
- `tankctl fields list`
- `tankctl locations list`
- `tankctl locations show LOC-101`
- `tankctl tanks list`
- `tankctl tanks at-risk --days 7`
- `tankctl tank status TK-101`
- `tankctl tank detail TK-101`
- `tankctl tank explain TK-101`
- `tankctl tank diagnostics TK-101`
- `tankctl tank alarms TK-101`
- `tankctl tank schedule TK-101`
- `tankctl alerts list --severity critical`
- `tankctl monitors health`

## MCP Surface

The MCP server exposes read-only tools for governed agent workflows:

- `get_portal_summary`
- `get_field_catalog`
- `list_tanks`
- `search_tanks`
- `get_tank_status`
- `get_tank_detail`
- `get_tank_diagnostics`
- `get_alarm_config`
- `get_call_schedule`
- `explain_delivery_priority`
- `list_runout_risks`
- `list_recent_alerts`
- `summarize_monitor_health`
- `list_locations`

## Synthetic Data Model

The demo models common industrial telemetry objects: organizations, locations, tanks, inventory readings, net/gross volume, volume percentage, available capacity, volume alarm status, communication status, sensor status, tank status, battery percentage, RSSI/signal health, synthetic serial/RTU-style IDs, alarm thresholds, call schedules, diagnostics, map points, runout risk, webhook events, and agent policy.

The JSON fixtures deliberately omit street addresses, users, emails, phone numbers, real device IDs, screenshots, logos, customer names, and proprietary records.

## Repo map

```text
src/tankdemo/api.py          FastAPI REST API
src/tankdemo/cli.py          Typer CLI exposed as tankctl
src/tankdemo/mcp_server.py   Read-only MCP server tools
src/tankdemo/risk.py         Alarm/risk/diagnostic summary logic
data/                        Synthetic organizations, locations, tanks, readings, alerts, field catalog
docs/                        Brief, email, architecture, security, demo script, field map
site/index.html              Static landing page for quick publishing
vercel.json                  Static Vercel route for the landing page
```

## How to verify the work

1. Clone the repo.
2. Create and activate a virtual environment with `python3 -m venv .venv` and `source .venv/bin/activate`.
3. Run `python -m pip install -e '.[dev,mcp]'` from the repo root.
4. Start the API with `python -m uvicorn tankdemo.api:app --reload`.
5. Open `/docs` and call `/summary`, `/tanks/{tank_id}/detail`, `/diagnostics`, and `/agent-policy`.
6. In another activated terminal, run the `tankctl` commands above.
7. Run `python -m pytest`.
8. Start the MCP server with `python -m tankdemo.mcp_server`.
9. Review `docs/security-model.md`, `docs/mcp-tools.md`, `docs/portal-field-map.md`, and `docs/one-page-brief.md`.

The API server runs in the foreground. Keep that terminal open while viewing `/docs`; use a second terminal for tests and CLI commands.

## Suggested next step

Use this demo as a conversation starter for a focused blueprint/prototype sprint: API surface map, CLI workflows, MCP tools/resources, webhook events, permissions, audit model, and phased implementation roadmap.
