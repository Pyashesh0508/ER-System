"""Attendance calculations and employee attendance metrics."""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

from app.config import (
    COL_EMP_ID,
    COL_NAME,
    COL_DEPT,
    COL_WORKING_DAYS,
    COL_PRESENT_DAYS,
    COL_ABSENT_DAYS,
    COL_LEAVE_DAYS,
    COL_ATTENDANCE_PCT,
    DEFAULT_ATTENDANCE_THRESHOLD,
)


def calculate_attendance_percentage(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate attendance percentage for each employee.

    Formula:
        Attendance Percentage = (Present_Days / Working_Days) * 100
        Rounded to 2 decimal places.

    Returns:
        DataFrame copy with Attendance_Percentage column added.
    """
    df_copy = df.copy()
    # Safe division avoiding zero division
    working = df_copy[COL_WORKING_DAYS].astype(float)
    present = df_copy[COL_PRESENT_DAYS].astype(float)

    pct = np.where(working > 0, (present / working) * 100.0, 0.0)
    df_copy[COL_ATTENDANCE_PCT] = np.round(pct, 2)
    return df_copy


def calculate_average_attendance(df: pd.DataFrame) -> float:
    """Calculate the average attendance percentage across all employees."""
    if df.empty:
        return 0.0
    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)
    return float(round(df[COL_ATTENDANCE_PCT].mean(), 2))


def get_highest_attendance_employee(df: pd.DataFrame) -> pd.DataFrame:
    """Return employee record(s) with the highest attendance percentage."""
    if df.empty:
        return pd.DataFrame()
    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)
    max_val = df[COL_ATTENDANCE_PCT].max()
    return df[df[COL_ATTENDANCE_PCT] == max_val].copy()


def get_lowest_attendance_employee(df: pd.DataFrame) -> pd.DataFrame:
    """Return employee record(s) with the lowest attendance percentage."""
    if df.empty:
        return pd.DataFrame()
    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)
    min_val = df[COL_ATTENDANCE_PCT].min()
    return df[df[COL_ATTENDANCE_PCT] == min_val].copy()


def get_low_attendance_employees(
    df: pd.DataFrame, threshold: float = DEFAULT_ATTENDANCE_THRESHOLD
) -> pd.DataFrame:
    """Return employees whose attendance percentage is strictly below the given threshold.

    Sorted by attendance percentage ascending.
    """
    if df.empty:
        return pd.DataFrame()
    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)
    low_df = df[df[COL_ATTENDANCE_PCT] < threshold].copy()
    return low_df.sort_values(by=COL_ATTENDANCE_PCT, ascending=True)


def get_high_attendance_employees(
    df: pd.DataFrame, benchmark: float = 90.0
) -> pd.DataFrame:
    """Return employees whose attendance percentage is greater than or equal to benchmark.

    Sorted by attendance percentage descending.
    """
    if df.empty:
        return pd.DataFrame()
    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)
    high_df = df[df[COL_ATTENDANCE_PCT] >= benchmark].copy()
    return high_df.sort_values(by=COL_ATTENDANCE_PCT, ascending=False)


def calculate_present_rate(df: pd.DataFrame) -> float:
    """Calculate the overall present rate across all employee days.

    (Total Present Days / Total Working Days) * 100
    """
    total_working = df[COL_WORKING_DAYS].sum()
    if total_working == 0:
        return 0.0
    return float(round((df[COL_PRESENT_DAYS].sum() / total_working) * 100.0, 2))


def calculate_absence_rate(df: pd.DataFrame) -> float:
    """Calculate the overall absence rate across all employee days.

    (Total Absent Days / Total Working Days) * 100
    """
    total_working = df[COL_WORKING_DAYS].sum()
    if total_working == 0:
        return 0.0
    return float(round((df[COL_ABSENT_DAYS].sum() / total_working) * 100.0, 2))


def calculate_leave_rate(df: pd.DataFrame) -> float:
    """Calculate the overall leave rate across all employee days.

    (Total Leave Days / Total Working Days) * 100
    """
    total_working = df[COL_WORKING_DAYS].sum()
    if total_working == 0:
        return 0.0
    return float(round((df[COL_LEAVE_DAYS].sum() / total_working) * 100.0, 2))


def get_attendance_summary_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """Compile comprehensive KPI metrics for attendance dashboard."""
    if df.empty:
        return {
            "total_employees": 0,
            "average_attendance": 0.0,
            "total_working_days": 0,
            "total_present_days": 0,
            "total_absent_days": 0,
            "total_leave_days": 0,
            "present_rate": 0.0,
            "absence_rate": 0.0,
            "leave_rate": 0.0,
            "highest_attendance": 0.0,
            "lowest_attendance": 0.0,
            "highest_employee_name": "N/A",
            "lowest_employee_name": "N/A",
        }

    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)

    highest_emp = get_highest_attendance_employee(df)
    lowest_emp = get_lowest_attendance_employee(df)

    highest_names = (
        ", ".join(highest_emp[COL_NAME].tolist()) if not highest_emp.empty else "N/A"
    )
    lowest_names = (
        ", ".join(lowest_emp[COL_NAME].tolist()) if not lowest_emp.empty else "N/A"
    )

    return {
        "total_employees": int(len(df)),
        "average_attendance": calculate_average_attendance(df),
        "total_working_days": int(df[COL_WORKING_DAYS].sum()),
        "total_present_days": int(df[COL_PRESENT_DAYS].sum()),
        "total_absent_days": int(df[COL_ABSENT_DAYS].sum()),
        "total_leave_days": int(df[COL_LEAVE_DAYS].sum()),
        "present_rate": calculate_present_rate(df),
        "absence_rate": calculate_absence_rate(df),
        "leave_rate": calculate_leave_rate(df),
        "highest_attendance": float(df[COL_ATTENDANCE_PCT].max()),
        "lowest_attendance": float(df[COL_ATTENDANCE_PCT].min()),
        "highest_employee_name": highest_names,
        "lowest_employee_name": lowest_names,
    }
