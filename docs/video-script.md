# 2–3 Minute Demo Video Script

## 0:00–0:20 — Setup

“I built a synthetic tank telemetry proof of concept showing how an industrial telemetry platform could expose secure API, CLI, webhook, and MCP surfaces. It uses synthetic data only and does not touch any vendor or customer system.”

## 0:20–0:55 — API

Open `/docs`. Show:

- `/summary`
- `/tanks/TK-101/detail`
- `/tanks/TK-101/diagnostics`
- `/tanks/TK-101/alarm-config`
- `/runout-risk?days=7`
- `/agent-policy`

Say: “The important part is the field-aware model: inventory, net/gross volume, alarm state, communication status, sensor status, battery, RSSI, thresholds, call schedule, and location context.”

## 0:55–1:35 — CLI

Run:

```bash
tankctl summary
tankctl tanks at-risk --days 7
tankctl tank explain TK-101
tankctl tank diagnostics TK-101
tankctl monitors health
```

Say: “This is useful for support, diagnostics, integration validation, and repeatable internal workflows.”

## 1:35–2:20 — MCP / Agent

Show the MCP tools list or explain the tools:

- `get_portal_summary`
- `get_tank_detail`
- `explain_delivery_priority`
- `summarize_monitor_health`

Say: “The agent can answer operational questions, explain risk, and propose actions, but it cannot change thresholds, move tanks, create delivery orders, or notify customers without explicit permissions and human approval.”

## 2:20–3:00 — Close

“This isn’t a rip-and-replace. It’s a way to make the existing telemetry layer programmable and agent-ready through a governed platform surface.”
