"""Tests for attendance percentage and metric calculations."""

import pandas as pd
from app.analysis.attendance import (
    calculate_attendance_percentage,
    calculate_average_attendance,
    get_highest_attendance_employee,
    get_lowest_attendance_employee,
    get_low_attendance_employees,
    calculate_present_rate,
    calculate_absence_rate,
)


def test_attendance_percentage_exact_formula():
    """Verify exact attendance percentage calculation matching prompt requirement.

    Present_Days = 20, Working_Days = 25 -> Attendance_Percentage = 80.0
    """
    df = pd.DataFrame({
        "Employee_ID": ["EMP001"],
        "Name": ["John Doe"],
        "Department": ["Engineering"],
        "Working_Days": [25],
        "Present_Days": [20],
        "Absent_Days": [3],
        "Leave_Days": [2],
    })

    result_df = calculate_attendance_percentage(df)
    assert "Attendance_Percentage" in result_df.columns
    assert result_df.loc[0, "Attendance_Percentage"] == 80.0


def test_average_attendance():
    """Verify company average attendance calculation."""
    df = pd.DataFrame({
        "Employee_ID": ["EMP001", "EMP002"],
        "Name": ["Alice", "Bob"],
        "Department": ["IT", "HR"],
        "Working_Days": [20, 20],
        "Present_Days": [20, 16],  # 100% and 80%
        "Absent_Days": [0, 2],
        "Leave_Days": [0, 2],
    })

    avg = calculate_average_attendance(df)
    assert avg == 90.0


def test_low_attendance_filtering():
    """Verify identification of employees below the configurable threshold."""
    df = pd.DataFrame({
        "Employee_ID": ["EMP001", "EMP002", "EMP003"],
        "Name": ["High", "Borderline", "Low"],
        "Department": ["IT", "IT", "Sales"],
        "Working_Days": [25, 25, 25],
        "Present_Days": [24, 20, 17],  # 96%, 80%, 68%
        "Absent_Days": [1, 5, 6],
        "Leave_Days": [0, 0, 2],
    })

    # Default threshold: 80% (strictly below 80%)
    low_df = get_low_attendance_employees(df, threshold=80.0)
    assert len(low_df) == 1
    assert low_df.iloc[0]["Employee_ID"] == "EMP003"
    assert low_df.iloc[0]["Attendance_Percentage"] == 68.0


def test_highest_and_lowest_attendance_employee():
    """Verify identifying highest and lowest attendance records."""
    df = pd.DataFrame({
        "Employee_ID": ["EMP001", "EMP002", "EMP003"],
        "Name": ["Alice", "Bob", "Charlie"],
        "Department": ["IT", "HR", "Sales"],
        "Working_Days": [20, 20, 20],
        "Present_Days": [20, 18, 14],  # 100%, 90%, 70%
        "Absent_Days": [0, 1, 4],
        "Leave_Days": [0, 1, 2],
    })

    highest = get_highest_attendance_employee(df)
    lowest = get_lowest_attendance_employee(df)

    assert highest.iloc[0]["Name"] == "Alice"
    assert highest.iloc[0]["Attendance_Percentage"] == 100.0

    assert lowest.iloc[0]["Name"] == "Charlie"
    assert lowest.iloc[0]["Attendance_Percentage"] == 70.0


def test_rates_calculation():
    """Verify overall present and absence rate calculations."""
    df = pd.DataFrame({
        "Employee_ID": ["EMP001", "EMP002"],
        "Name": ["Alice", "Bob"],
        "Department": ["IT", "HR"],
        "Working_Days": [20, 20],  # Total 40
        "Present_Days": [18, 14],  # Total 32 -> 80.0%
        "Absent_Days": [2, 4],    # Total 6  -> 15.0%
        "Leave_Days": [0, 2],     # Total 2  -> 5.0%
    })

    assert calculate_present_rate(df) == 80.0
    assert calculate_absence_rate(df) == 15.0
