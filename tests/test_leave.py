"""Tests for leave metrics and patterns."""

import pandas as pd
from app.analysis.leave import (
    calculate_leave_summary,
    get_employees_by_leave_bracket,
)


def test_leave_summary_calculations():
    """Verify aggregated leave metrics and top leave employee identification."""
    df = pd.DataFrame({
        "Employee_ID": ["E1", "E2", "E3"],
        "Name": ["Alice", "Bob", "Charlie"],
        "Department": ["Tech", "Sales", "Tech"],
        "Working_Days": [20, 20, 20],
        "Present_Days": [19, 15, 17],
        "Absent_Days": [1, 1, 1],
        "Leave_Days": [0, 4, 2],
    })

    summary = calculate_leave_summary(df)
    assert summary["total_leave_days"] == 6
    assert summary["avg_leave_per_employee"] == 2.0
    assert summary["max_leave_days"] == 4
    assert summary["min_leave_days"] == 0
    assert "Bob" in summary["top_leave_employees"]


def test_leave_summary_with_department_filter():
    """Verify department filtering in leave metrics."""
    df = pd.DataFrame({
        "Employee_ID": ["E1", "E2", "E3"],
        "Name": ["Alice", "Bob", "Charlie"],
        "Department": ["Tech", "Sales", "Tech"],
        "Working_Days": [20, 20, 20],
        "Present_Days": [19, 15, 17],
        "Absent_Days": [1, 1, 1],
        "Leave_Days": [1, 5, 3],
    })

    summary_tech = calculate_leave_summary(df, department_filter="Tech")
    assert summary_tech["total_leave_days"] == 4
    assert summary_tech["avg_leave_per_employee"] == 2.0
    assert summary_tech["max_leave_days"] == 3


def test_leave_brackets_assignment():
    """Verify proper assignment into leave brackets."""
    df = pd.DataFrame({
        "Employee_ID": ["E1", "E2", "E3", "E4"],
        "Name": ["A", "B", "C", "D"],
        "Department": ["Tech", "Tech", "Tech", "Tech"],
        "Working_Days": [20, 20, 20, 20],
        "Present_Days": [20, 18, 16, 14],
        "Absent_Days": [0, 0, 0, 0],
        "Leave_Days": [0, 2, 4, 6],
    })

    bracket_df = get_employees_by_leave_bracket(df)
    assert bracket_df.loc[0, "Leave_Bracket"] == "0 Days (No Leave)"
    assert bracket_df.loc[1, "Leave_Bracket"] == "1-2 Days"
    assert bracket_df.loc[2, "Leave_Bracket"] == "3-4 Days"
    assert bracket_df.loc[3, "Leave_Bracket"] == "5+ Days"
