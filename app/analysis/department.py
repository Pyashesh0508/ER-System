"""Department-level attendance and workforce analysis."""

from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np

from app.config import (
    COL_DEPT,
    COL_WORKING_DAYS,
    COL_PRESENT_DAYS,
    COL_ABSENT_DAYS,
    COL_LEAVE_DAYS,
    COL_ATTENDANCE_PCT,
)
from app.analysis.attendance import calculate_attendance_percentage


def get_department_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Compute aggregate attendance statistics by department.

    Returns a DataFrame with:
    - Department
    - Employee_Count
    - Average_Attendance_Pct
    - Total_Working_Days
    - Total_Present_Days
    - Total_Absent_Days
    - Total_Leave_Days
    - Avg_Present_Days
    - Avg_Absent_Days
    - Avg_Leave_Days
    """
    if df.empty:
        return pd.DataFrame()

    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)

    grouped = df.groupby(COL_DEPT).agg(
        Employee_Count=(COL_DEPT, "count"),
        Average_Attendance_Pct=(COL_ATTENDANCE_PCT, "mean"),
        Total_Working_Days=(COL_WORKING_DAYS, "sum"),
        Total_Present_Days=(COL_PRESENT_DAYS, "sum"),
        Total_Absent_Days=(COL_ABSENT_DAYS, "sum"),
        Total_Leave_Days=(COL_LEAVE_DAYS, "sum"),
        Avg_Present_Days=(COL_PRESENT_DAYS, "mean"),
        Avg_Absent_Days=(COL_ABSENT_DAYS, "mean"),
        Avg_Leave_Days=(COL_LEAVE_DAYS, "mean"),
    ).reset_index()

    grouped["Average_Attendance_Pct"] = grouped["Average_Attendance_Pct"].round(2)
    grouped["Avg_Present_Days"] = grouped["Avg_Present_Days"].round(2)
    grouped["Avg_Absent_Days"] = grouped["Avg_Absent_Days"].round(2)
    grouped["Avg_Leave_Days"] = grouped["Avg_Leave_Days"].round(2)

    return grouped.sort_values(by="Average_Attendance_Pct", ascending=False)


def get_department_extremes(
    dept_summary_df: pd.DataFrame,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Find the highest and lowest attendance departments.

    Returns:
        (highest_dept_dict, lowest_dept_dict)
    """
    if dept_summary_df.empty:
        empty = {"Department": "N/A", "Average_Attendance_Pct": 0.0}
        return empty, empty

    max_idx = dept_summary_df["Average_Attendance_Pct"].idxmax()
    min_idx = dept_summary_df["Average_Attendance_Pct"].idxmin()

    highest = dept_summary_df.loc[max_idx].to_dict()
    lowest = dept_summary_df.loc[min_idx].to_dict()
    return highest, lowest


def get_department_leave_extremes(
    dept_summary_df: pd.DataFrame,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Find the departments with highest and lowest average leave days."""
    if dept_summary_df.empty:
        empty = {"Department": "N/A", "Avg_Leave_Days": 0.0}
        return empty, empty

    max_idx = dept_summary_df["Avg_Leave_Days"].idxmax()
    min_idx = dept_summary_df["Avg_Leave_Days"].idxmin()

    highest = dept_summary_df.loc[max_idx].to_dict()
    lowest = dept_summary_df.loc[min_idx].to_dict()
    return highest, lowest


def get_employees_in_department(df: pd.DataFrame, department: str) -> pd.DataFrame:
    """Filter records for a specific department."""
    if df.empty or not department:
        return pd.DataFrame()
    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)
    return df[df[COL_DEPT] == department].copy()
