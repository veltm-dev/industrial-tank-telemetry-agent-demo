# Industrial Tank Telemetry Agent Demo

An independent, synthetic concept demo showing how industrial tank telemetry workflows can be exposed through governed **API**, **CLI**, **webhook**, and **MCP** surfaces.

The core idea is simple:

> The portal is for humans. The API is for software. The CLI is for repeatable operator, support, and engineering workflows. The MCP server is for approved AI agents. Governance keeps high-risk actions behind permissions, audit logs, and human approval.

## Public posture

This repository is a **non-proprietary architecture and workflow demo**. It is intended to make a product/platform idea inspectable through working code, synthetic fixtures, tests, and documentation.

It is **not** an official vendor project, not a clone of any commercial platform, not a reverse-engineered system, and not connected to any real customer, device, portal, or production environment.

This demo uses synthetic data only. It does **not** access AMETEK, Telular, SkyBitz, SmartTank, customer systems, customer records, proprietary portals, screenshots, logos, addresses, users, phone numbers, emails, or real device records. It is not affiliated with or endorsed by those companies.

## What this demonstrates

Industrial tank telemetry systems already collect operationally valuable data: inventory, alarms, diagnostics, call schedules, device status, locations, products, route context, and runout risk.

This demo shows how that kind of telemetry layer could become safely programmable without replacing an existing human-facing portal:

- **REST API** for structured access to summaries, organizations, locations, tanks, readings, alerts, diagnostics, alarm configuration, call schedules, map points, webhook events, runout risk, and agent policy.
- **CLI** for repeatable support, product, field-operations, QA, and integration workflows.
- **MCP server** for read-only, tool-based AI/agent access to approved operational questions.
- **Webhook/event model** for external systems that need to react to telemetry changes.
- **Governance model** that separates read, recommend, human-approved write, and restricted/admin actions.

The goal is not “replace the portal with AI.” The goal is to demonstrate a governed programmable layer around telemetry data and operational workflows.

## What this is not

This project is intentionally limited in scope.

It is not:

- a production SaaS application
- a replacement for any existing tank-monitoring portal
- a SmartTank clone
- an AMETEK, Telular, SkyBitz, or SmartTank integration
- connected to live tank monitors, gateways, customers, maps, dispatch systems, or ERPs
- using real customer data, real addresses, real user records, real device IDs, screenshots, or proprietary exports
- designed to perform operational writes such as changing thresholds, acknowledging alarms, notifying customers, changing routes, or creating delivery orders

The demo is read-only by default. In a production system, write actions would require explicit scopes, tenant-aware authorization, audit logging, and human approval where appropriate.

## Live links

- GitHub repo: <https://github.com/veltm-dev/industrial-tank-telemetry-agent-demo>
- Static landing page: <https://industrial-tank-telemetry-agent-dem.vercel.app>

## How the pieces fit

| Surface | Primary user | What it proves |
|---|---|---|
| REST API | Software systems and integration teams | Telemetry can be exposed as stable, structured resources. |
| CLI | Support, operations, QA, product, and engineering teams | Common workflows can become repeatable commands instead of manual portal clicks. |
| MCP server | Approved AI agents and assistant workflows | Agents can retrieve and explain approved telemetry data without broad system access. |
| Webhooks | Dispatch, ERP, alerting, and downstream systems | External systems can react to operational events. |
| Agent policy | Product, security, compliance, and platform owners | Read/recommend/write/admin boundaries can be explicit from the beginning. |

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

Open the API docs:

```text
http://localhost:8000/docs
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

Run the static landing page locally by opening:

```text
site/index.html
```

## API examples

```bash
curl http://localhost:8000/summary
curl http://localhost:8000/field-catalog
curl http://localhost:8000/organizations
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

## CLI examples

The CLI is intentionally read-only and optimized for inspection:

```bash
tankctl summary
tankctl fields list
tankctl locations list
tankctl locations show LOC-101
tankctl tanks list
tankctl tanks at-risk --days 7
tankctl tank status TK-101
tankctl tank detail TK-101
tankctl tank explain TK-101
tankctl tank diagnostics TK-101
tankctl tank alarms TK-101
tankctl tank schedule TK-101
tankctl alerts list --severity critical
tankctl monitors health
```

Example operator/support question:

> Which tanks need human review in the next seven days, and why?

Equivalent CLI workflow:

```bash
tankctl tanks at-risk --days 7
tankctl tank explain TK-101
tankctl tank diagnostics TK-101
```

## MCP surface

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

The MCP layer does not give an agent unrestricted database or browser access. It exposes a controlled set of named tools that map to approved read-only workflows.

Human CLI command to MCP tool mapping:

| Human CLI command | Agent/MCP tool |
|---|---|
| `tankctl summary` | `get_portal_summary` |
| `tankctl tanks at-risk --days 7` | `list_runout_risks(days=7)` |
| `tankctl tank explain TK-101` | `explain_delivery_priority("TK-101")` |
| `tankctl tank diagnostics TK-101` | `get_tank_diagnostics("TK-101")` |
| `tankctl monitors health` | `summarize_monitor_health` |

## Synthetic data model

The demo models common industrial telemetry concepts:

- organizations and locations
- tanks and products
- inventory readings
- net/gross volume
- volume percentage
- available capacity
- volume alarm status
- communication status
- sensor status
- tank status
- battery percentage
- RSSI / signal health
- synthetic serial / RTU-style identifiers
- alarm thresholds
- call schedules
- diagnostic information
- map points
- runout risk
- webhook events
- agent policy

The fixtures deliberately omit real street addresses, users, emails, phone numbers, real device IDs, screenshots, logos, customer names, and proprietary records.

## Governance posture

This demo treats agent access as a controlled platform surface, not an open-ended automation shortcut.

Suggested production permission levels:

1. **Read** — summary, tank status, diagnostics, alerts, locations, field catalog.
2. **Recommend** — explain delivery priority, suggest dispatch review, flag monitor-health issues, draft internal notes.
3. **Human-approved write** — acknowledge alert, create delivery order, notify customer, change route, edit alarm threshold.
4. **Restricted/admin** — user permissions, sensitive exports, tenant configuration, device/system configuration.

This repository implements the safe starting point: read-only retrieval and explanation over synthetic telemetry.

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
5. Open `/docs` and call `/summary`, `/tanks/{tank_id}/detail`, `/diagnostics`, `/runout-risk`, and `/agent-policy`.
6. In another activated terminal, run the `tankctl` commands above.
7. Run `python -m pytest`.
8. Start the MCP server with `python -m tankdemo.mcp_server`.
9. Review `docs/security-model.md`, `docs/mcp-tools.md`, `docs/portal-field-map.md`, and `docs/one-page-brief.md`.

The API server runs in the foreground. Keep that terminal open while viewing `/docs`; use a second terminal for tests and CLI commands.

## Possible extensions

This concept could be extended into a formal blueprint or prototype by mapping a real product’s approved object model, integration requirements, permission boundaries, webhook events, customer workflows, internal support workflows, and audit requirements.

Any production version should start with security, tenant isolation, data minimization, permissions, audit trails, and human-approval boundaries before enabling write actions.
