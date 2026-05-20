import re

from typer.testing import CliRunner

from tankdemo import data
from tankdemo.cli import app

runner = CliRunner()


def test_required_cli_commands_work():
    commands = [
        ["summary"],
        ["fields", "list"],
        ["locations", "list"],
        ["locations", "show", "LOC-101"],
        ["tanks", "list"],
        ["tanks", "at-risk", "--days", "7"],
        ["tank", "status", "TK-101"],
        ["tank", "detail", "TK-101"],
        ["tank", "explain", "TK-101"],
        ["tank", "diagnostics", "TK-101"],
        ["tank", "alarms", "TK-101"],
        ["tank", "schedule", "TK-101"],
        ["alerts", "list", "--severity", "critical"],
        ["monitors", "health"],
    ]

    for command in commands:
        result = runner.invoke(app, command)
        assert result.exit_code == 0, f"{command}: {result.output}"


def test_mcp_tool_functions_return_read_only_data():
    from tankdemo import mcp_server

    summary = mcp_server.get_portal_summary()
    detail = mcp_server.get_tank_detail("TK-101")
    policy = mcp_server.agent_safety_policy()

    assert summary["total_tanks"] >= 8
    assert detail["tank"]["id"] == "TK-101"
    assert "read-only" in policy


def test_synthetic_data_has_no_real_contact_or_address_values():
    forbidden_patterns = [
        re.compile(r"\b\d{3,5}\s+[A-Za-z0-9 .'-]+(?:Ave|Avenue|Rd|Road|St|Street|Blvd|Boulevard|Way)\b"),
        re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+"),
        re.compile(r"\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"),
    ]
    forbidden_terms = {
        "Hemet",
        "Menifee",
        "Riverside",
        "Orange County",
        "Sun Valley",
        "Pacific Demo Fuels",
        "Western Demo Energy",
    }

    payloads = [data.organizations(), data.locations(), data.tanks(), data.alerts(), data.readings()]
    haystack = repr(payloads)

    for pattern in forbidden_patterns:
        assert not pattern.search(haystack)
    for term in forbidden_terms:
        assert term not in haystack


def test_organization_counts_match_tanks():
    tanks = data.tanks()
    for organization in data.organizations():
        direct_count = sum(1 for tank in tanks if tank["organization_id"] == organization["id"])
        assert organization["tank_count"] == direct_count


def test_location_addresses_are_intentionally_omitted():
    assert all(location["address"] is None for location in data.locations())
    assert all(tank["address"] is None for tank in data.tanks())
