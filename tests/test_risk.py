from tankdemo import data
from tankdemo.risk import explain_priority, portal_summary, risk_level, runout_risk


def test_critical_tank_is_detected():
    tank = data.get_tank("TK-101")
    assert tank is not None
    assert risk_level(tank) == "critical"
    explanation = explain_priority(tank)
    assert explanation["human_review_required"] is True
    assert "Critical Low Alarm" in explanation["volume_alarm_status"]


def test_runout_risk_window_finds_expected_tanks():
    rows = runout_risk(data.tanks(), days=7)
    ids = {row["tank_id"] for row in rows}
    assert "TK-101" in ids
    assert "TK-105" in ids


def test_portal_summary_counts():
    summary = portal_summary(data.tanks(), data.alerts())
    assert summary["total_tanks"] == len(data.tanks())
    assert summary["volume_alarm_counts"]["Critical Low Alarm"] >= 2
