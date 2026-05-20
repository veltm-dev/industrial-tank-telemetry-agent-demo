# Agent-Ready Tank Telemetry Concept — API + CLI + MCP

## Thesis

Tank telemetry systems already contain the operational data: inventory, alarm status, communication health, sensor health, locations, devices, routes, thresholds, and delivery forecasting parameters. The next platform step is making that data safely programmable.

## What this synthetic demo shows

- REST API for summaries, tanks, locations, diagnostics, alarm config, call schedules, alerts, readings, map points, and runout risk.
- CLI for support, diagnostics, integration validation, and field-operations workflows.
- MCP server exposing read-only tools to AI agents.
- Webhook/event model for integrations.
- Agent policy with read-only defaults, write-action boundaries, audit logging, and human approval.

## Why it matters

A portal helps users view data. A programmable platform helps customers, internal teams, dispatch systems, integration partners, and agents act on that data safely.

## Suggested engagement

Start with a fixed-scope blueprint/prototype sprint:

1. Field/object model map
2. API endpoint design
3. CLI workflow design
4. MCP tool/resource design
5. Webhook/event model
6. Permission/audit model
7. Phased implementation roadmap

## Disclaimer

This proof of concept uses synthetic data only. It does not access AMETEK, Telular, SkyBitz, SmartTank, customer systems, proprietary portals, screenshots, logos, customer names, street addresses, users, emails, phone numbers, real device IDs, or proprietary services. It is not affiliated with or endorsed by those companies.
