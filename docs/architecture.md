# Architecture

```text
Synthetic data
  ├─ organizations.json
  ├─ locations.json
  ├─ tanks.json
  ├─ readings.json
  ├─ alerts.json
  └─ field_catalog.json
        │
        ▼
Risk + summary layer
  ├─ portal summary
  ├─ runout/empty-limit risk
  ├─ delivery priority explanation
  ├─ monitor health summary
  └─ diagnostics extraction
        │
        ├──────────────► FastAPI REST API
        │
        ├──────────────► tankctl CLI
        │
        └──────────────► read-only MCP server
```

The fixture data is deliberately synthetic. It models field shape and workflow context without street addresses, real customer names, users, emails, phone numbers, screenshots, logos, proprietary records, or real device IDs.

## Production direction

A production system would replace synthetic JSON with platform data services, introduce identity and authorization, apply tenant/org scoping, emit event streams/webhooks, write audit logs, and put all mutating actions behind explicit permissions and human approval.
