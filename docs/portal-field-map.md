# Portal Field Map → API/CLI/MCP Surface

This document maps a typical tank telemetry field model into modern programmable surfaces. It uses synthetic examples only and does not contain customer records, street addresses, proprietary portal data, screenshots, logos, users, emails, phone numbers, or real device identifiers.

## Core objects

- `Organization`: company, parent organization, active flag, customer/user IDs
- `Location`: address field, city/state fields, country, timezone, active days, role-based contact label, number of tanks, delivery forecasting parameters. The demo data intentionally omits street addresses.
- `Tank`: tank name, tank number, product, capacity, level, net/gross inventory, available capacity, percentage full/empty, route, region
- `Device / RTU`: serial/RTU ID, cellular/MIN ID, model, firmware, carrier, battery, RSSI, call count, failed calls, transmit/ack sequence
- `Alarm config`: low/high/critical thresholds, temperature thresholds, fill detect, short fill amount, reorder level, safety stock
- `Event`: inventory update, alarm state changed, no recent update, delivery detected, short fill, monitor health changed

## API resources

```text
GET /summary
GET /field-catalog
GET /organizations
GET /locations
GET /locations/{location_id}
GET /tanks
GET /tanks/{tank_id}/detail
GET /tanks/{tank_id}/status
GET /tanks/{tank_id}/diagnostics
GET /tanks/{tank_id}/alarm-config
GET /tanks/{tank_id}/call-schedule
GET /readings?tank_id=TK-101
GET /alerts?severity=critical
GET /runout-risk?days=7
GET /monitor-health
GET /map-points
GET /webhook-events
GET /agent-policy
```

## CLI workflows

```bash
tankctl summary
tankctl fields list
tankctl locations list
tankctl locations show LOC-101
tankctl tanks list
tankctl tanks at-risk --days 7
tankctl tank detail TK-101
tankctl tank diagnostics TK-101
tankctl tank alarms TK-101
tankctl tank schedule TK-101
tankctl monitors health
```

## MCP tools

```text
get_portal_summary
get_field_catalog
list_tanks
search_tanks
get_tank_status
get_tank_detail
get_tank_diagnostics
get_alarm_config
get_call_schedule
explain_delivery_priority
list_runout_risks
list_recent_alerts
summarize_monitor_health
list_locations
```

## Write actions intentionally excluded

The demo does not implement write actions. In a production system, the following should require explicit scopes, audit logs, and usually human approval:

- Move tank to another location
- Edit alarm thresholds
- Edit call schedules
- Acknowledge or suppress alarms
- Create delivery orders
- Notify customers
- Edit users, groups, roles, or permissions
- Export customer-identifiable data
