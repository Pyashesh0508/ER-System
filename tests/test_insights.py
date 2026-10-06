"""Tests for workforce insights generator."""

import pandas as pd
from app.analysis.insights import generate_workforce_insights


def test_generate_workforce_insights_healthy():
    """Verify healthy workforce insights generation."""
    df = pd.DataFrame({
        "Employee_ID": ["E1", "E2"],
        "Name": ["Alice", "Bob"],
        "Department": ["Tech", "HR"],
        "Working_Days": [25, 25],
        "Present_Days": [24, 25],  # 96% and 100%
        "Absent_Days": [0, 0],
        "Leave_Days": [1, 0],
    })

    insights = generate_workforce_insights(df, threshold=80.0)
    assert len(insights) >= 2
    assert any(i["type"] == "success" for i in insights)
    assert any("Healthy Workforce Attendance" in i["title"] for i in insights)


def test_generate_workforce_insights_low_attendance_alert():
    """Verify threshold alert generation when employees fall below threshold."""
    df = pd.DataFrame({
        "Employee_ID": ["E1", "E2"],
        "Name": ["Alice", "Bob"],
        "Department": ["Tech", "HR"],
        "Working_Days": [25, 25],
        "Present_Days": [24, 15],  # 96% and 60%
        "Absent_Days": [1, 8],
        "Leave_Days": [0, 2],
    })

    insights = generate_workforce_insights(df, threshold=80.0)
    assert any("Employees Below Threshold" in i["title"] for i in insights)
    assert any("Bob" in i["message"] for i in insights)
