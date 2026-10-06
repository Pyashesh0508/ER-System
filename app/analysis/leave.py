"""Leave patterns and metrics analysis."""

from typing import Dict, Any, Optional
import pandas as pd

from app.config import (
    COL_EMP_ID,
    COL_NAME,
    COL_DEPT,
    COL_LEAVE_DAYS,
    COL_WORKING_DAYS,
)
from app.analysis.department import get_department_summary


def calculate_leave_summary(
    df: pd.DataFrame, department_filter: Optional[str] = None
) -> Dict[str, Any]:
    """Calculate key leave statistics, optionally filtered by department.

    Returns:
        Dictionary with total, average, min, max leave days, and top employee.
    """
    if df.empty:
        return {
            "total_leave_days": 0,
            "avg_leave_per_employee": 0.0,
            "max_leave_days": 0,
            "min_leave_days": 0,
            "top_leave_employees": "N/A",
            "department_highest_leave": "N/A",
            "department_lowest_leave": "N/A",
        }

    filtered_df = df.copy()
    if department_filter and department_filter != "All":
        filtered_df = filtered_df[filtered_df[COL_DEPT] == department_filter]

    if filtered_df.empty:
        return {
            "total_leave_days": 0,
            "avg_leave_per_employee": 0.0,
            "max_leave_days": 0,
            "min_leave_days": 0,
            "top_leave_employees": "None",
            "department_highest_leave": "N/A",
            "department_lowest_leave": "N/A",
        }

    total_leave = int(filtered_df[COL_LEAVE_DAYS].sum())
    avg_leave = round(float(filtered_df[COL_LEAVE_DAYS].mean()), 2)
    max_leave = int(filtered_df[COL_LEAVE_DAYS].max())
    min_leave = int(filtered_df[COL_LEAVE_DAYS].min())

    # Employees with maximum leave
    top_leave_subset = filtered_df[filtered_df[COL_LEAVE_DAYS] == max_leave]
    top_leave_names = ", ".join(top_leave_subset[COL_NAME].tolist()) if not top_leave_subset.empty else "N/A"

    # Department extremes across overall dataset
    dept_summary = get_department_summary(df)
    dept_high = "N/A"
    dept_low = "N/A"
    if not dept_summary.empty:
        high_idx = dept_summary["Total_Leave_Days"].idxmax()
        low_idx = dept_summary["Total_Leave_Days"].idxmin()
        dept_high = f"{dept_summary.loc[high_idx, COL_DEPT]} ({dept_summary.loc[high_idx, 'Total_Leave_Days']} days)"
        dept_low = f"{dept_summary.loc[low_idx, COL_DEPT]} ({dept_summary.loc[low_idx, 'Total_Leave_Days']} days)"

    return {
        "total_leave_days": total_leave,
        "avg_leave_per_employee": avg_leave,
        "max_leave_days": max_leave,
        "min_leave_days": min_leave,
        "top_leave_employees": top_leave_names,
        "department_highest_leave": dept_high,
        "department_lowest_leave": dept_low,
    }


def get_employees_by_leave_bracket(df: pd.DataFrame) -> pd.DataFrame:
    """Categorize employees into leave brackets for distribution analysis."""
    if df.empty:
        return pd.DataFrame()

    df_copy = df.copy()

    def categorize(days: float) -> str:
        if days == 0:
            return "0 Days (No Leave)"
        elif days <= 2:
            return "1-2 Days"
        elif days <= 4:
            return "3-4 Days"
        else:
            return "5+ Days"

    df_copy["Leave_Bracket"] = df_copy[COL_LEAVE_DAYS].apply(categorize)
    return df_copy
