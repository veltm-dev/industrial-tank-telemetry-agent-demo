# CLI Commands

The CLI is meant for support, integrations, technical account teams, and internal engineering workflows.

```bash
tankctl summary
tankctl fields list
tankctl locations list
tankctl locations show LOC-101
tankctl tanks list
tankctl tanks list --region "Demo Region North"
tankctl tanks at-risk --days 7
tankctl tank status TK-101
tankctl tank detail TK-101
tankctl tank diagnostics TK-101
tankctl tank alarms TK-101
tankctl tank schedule TK-101
tankctl tank explain TK-101
tankctl alerts list
tankctl alerts list --severity critical
tankctl monitors health
```

## Why a CLI matters

A portal is good for users. A CLI is good for repeatable support work, diagnostics, export validation, integration testing, and internal automation.

All command output is generated from synthetic fixtures. The demo intentionally omits street addresses, real customer names, users, emails, phone numbers, and real device IDs.
