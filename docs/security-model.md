# Security and Governance Model

This demo is read-only by default and uses synthetic data only. It does not include real users, phone numbers, emails, customer names, street addresses, proprietary device records, portal screenshots, logos, or scraped data.

## Example read scopes

- `summary:read`
- `organizations:read`
- `locations:read`
- `tanks:read`
- `readings:read`
- `alerts:read`
- `diagnostics:read`
- `alarm_config:read`
- `risk:read`
- `monitor_health:read`

## Write scopes that should require elevated controls

- `tanks:move`
- `alarms:write`
- `alerts:acknowledge`
- `dispatch_orders:write`
- `customers:notify`
- `users:write`
- `permissions:write`
- `exports:pii`

## Agent policy

Agents should be allowed to retrieve information and propose actions. They should not directly perform operational actions without explicit scope, audit logging, and human approval.

## Data handling boundary

The included JSON fixtures are demonstration records only. Production data would require tenant scoping, identity, authorization, retention controls, audit logging, export controls, and a documented approval path for any mutating workflow.

## Audit log fields

- Actor
- Tool or API endpoint
- Object ID
- Organization/location scope
- Timestamp
- Input arguments
- Output hash or result summary
- Human approval ID, if applicable
