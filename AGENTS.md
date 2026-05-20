# Codex Agent Instructions

## Mission
Build and polish a one-day credibility packet for an industrial tank telemetry API/CLI/MCP concept demo. The output should be suitable to send to an enterprise product or engineering manager today.

## Product-context direction
This repo should feel field-aware, not generic. Model common tank telemetry portal objects: organizations, locations, tanks, inventory, net/gross volume, available capacity, alarm status, comm status, sensor status, battery, RSSI, serial/RTU ID, diagnostics, alarm thresholds, call schedules, map points, and delivery forecasting parameters.

## Hard constraints
- Use synthetic data only.
- Do not claim affiliation with AMETEK, Telular, SkyBitz, SmartTank, or any customer.
- Do not use company logos, customer names, screenshots, scraped portal content, addresses, device IDs, or proprietary data.
- Keep the demo read-only by default.
- Do not expand into a full SaaS app, auth system, or production deployment.
- Make every deliverable inspectable: code, tests, docs, landing page, email.

## Done means
- `pip install -e '.[dev,mcp]'` works.
- `uvicorn tankdemo.api:app --reload` starts the API.
- `/docs` shows useful endpoints.
- `tankctl summary`, `tankctl tanks list`, `tankctl tanks at-risk --days 7`, `tankctl tank diagnostics TK-101`, and `tankctl tank explain TK-101` work.
- `python -m tankdemo.mcp_server` starts a read-only MCP server.
- `pytest` passes.
- The README explains what the demo proves and how to verify it.
- The docs include a one-page brief, email draft, video script, architecture, MCP tools, CLI commands, portal field map, and security model.
- The static landing page is professional and can be published quickly.

## Style
Use direct, executive-friendly language. The buyer should see operator workflow insight, not generic AI buzzwords. Emphasize governed programmability, not replacing the existing portal.
