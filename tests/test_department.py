"""Tests for department-level analytics."""

import pandas as pd
from app.analysis.department import (
    get_department_summary,
    get_department_extremes,
    get_department_leave_extremes,
    get_employees_in_department,
)


def test_department_summary_metrics():
    """Verify department grouping and average calculations."""
    df = pd.DataFrame({
        "Employee_ID": ["E1", "E2", "E3", "E4"],
        "Name": ["A", "B", "C", "D"],
        "Department": ["Tech", "Tech", "Sales", "Sales"],
        "Working_Days": [20, 20, 20, 20],
        "Present_Days": [20, 18, 16, 14],  # Tech: 100%, 90% (avg 95%); Sales: 80%, 70% (avg 75%)
        "Absent_Days": [0, 1, 2, 4],
        "Leave_Days": [0, 1, 2, 2],
    })

    dept_df = get_department_summary(df)
    assert len(dept_df) == 2
    tech_row = dept_df[dept_df["Department"] == "Tech"].iloc[0]
    sales_row = dept_df[dept_df["Department"] == "Sales"].iloc[0]

    assert tech_row["Employee_Count"] == 2
    assert tech_row["Average_Attendance_Pct"] == 95.0

    assert sales_row["Employee_Count"] == 2
    assert sales_row["Average_Attendance_Pct"] == 75.0


def test_department_extremes():
    """Verify detection of highest and lowest performing departments."""
    df = pd.DataFrame({
        "Employee_ID": ["E1", "E2"],
        "Name": ["A", "B"],
        "Department": ["HighDept", "LowDept"],
        "Working_Days": [20, 20],
        "Present_Days": [19, 15],  # 95% vs 75%
        "Absent_Days": [1, 3],
        "Leave_Days": [0, 2],
    })

    dept_summary = get_department_summary(df)
    highest, lowest = get_department_extremes(dept_summary)

    assert highest["Department"] == "HighDept"
    assert highest["Average_Attendance_Pct"] == 95.0
    assert lowest["Department"] == "LowDept"
    assert lowest["Average_Attendance_Pct"] == 75.0


def test_filter_employees_in_department():
    """Verify department member extraction."""
    df = pd.DataFrame({
        "Employee_ID": ["E1", "E2", "E3"],
        "Name": ["Alice", "Bob", "Charlie"],
        "Department": ["Tech", "HR", "Tech"],
        "Working_Days": [20, 20, 20],
        "Present_Days": [19, 18, 17],
        "Absent_Days": [1, 1, 2],
        "Leave_Days": [0, 1, 1],
    })

    members = get_employees_in_department(df, "Tech")
    assert len(members) == 2
    assert set(members["Name"].tolist()) == {"Alice", "Charlie"}
