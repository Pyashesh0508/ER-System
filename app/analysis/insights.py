"""Workforce insights module generating rule-based analytical observations."""

from typing import List, Dict, Any
import pandas as pd

from app.config import (
    DEFAULT_ATTENDANCE_THRESHOLD,
    HIGH_ATTENDANCE_BENCHMARK,
    COL_NAME,
    COL_DEPT,
    COL_ATTENDANCE_PCT,
    COL_LEAVE_DAYS,
    COL_ABSENT_DAYS,
)
from app.analysis.attendance import (
    calculate_attendance_percentage,
    calculate_average_attendance,
    get_low_attendance_employees,
    calculate_absence_rate,
    calculate_leave_rate,
)
from app.analysis.department import get_department_summary, get_department_extremes


def generate_workforce_insights(
    df: pd.DataFrame, threshold: float = DEFAULT_ATTENDANCE_THRESHOLD
) -> List[Dict[str, str]]:
    """Generate structured, rule-based analytical observations from attendance data.

    Returns a list of dictionaries with keys:
    - 'category': Area of insight (Overall, Department, Threshold, Leave, Absence)
    - 'type': 'success', 'warning', 'info', or 'alert'
    - 'title': Headline
    - 'message': Detailed analytical observation
    """
    insights: List[Dict[str, str]] = []

    if df.empty:
        return [
            {
                "category": "General",
                "type": "info",
                "title": "No Data Available",
                "message": "Dataset is empty. Load attendance data to view workforce insights.",
            }
        ]

    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)

    avg_attendance = calculate_average_attendance(df)
    total_employees = len(df)
    low_att_df = get_low_attendance_employees(df, threshold=threshold)
    low_att_count = len(low_att_df)
    absence_rate = calculate_absence_rate(df)
    leave_rate = calculate_leave_rate(df)

    # 1. Overall Attendance Health Insight
    if avg_attendance >= 88.0:
        insights.append({
            "category": "Overall Health",
            "type": "success",
            "title": "Healthy Workforce Attendance",
            "message": f"Overall average employee attendance stands at {avg_attendance:.2f}%, indicating a high level of operational stability and workforce engagement.",
        })
    elif avg_attendance >= 75.0:
        insights.append({
            "category": "Overall Health",
            "type": "info",
            "title": "Moderate Attendance Level",
            "message": f"Overall average employee attendance is {avg_attendance:.2f}%. While operations are stable, there is room for improvement in workforce consistency.",
        })
    else:
        insights.append({
            "category": "Overall Health",
            "type": "alert",
            "title": "Overall Attendance Requires Attention",
            "message": f"Overall average attendance is low at {avg_attendance:.2f}%. Management review of operational factors impacting attendance is recommended.",
        })

    # 2. Threshold & Risk Alerts
    if low_att_count > 0:
        low_att_pct = (low_att_count / total_employees) * 100.0
        emp_names = ", ".join(low_att_df[COL_NAME].head(3).tolist())
        suffix = f" and {low_att_count - 3} others" if low_att_count > 3 else ""
        insights.append({
            "category": "Attendance Threshold",
            "type": "warning",
            "title": f"Employees Below Threshold ({threshold:.0f}%)",
            "message": (
                f"{low_att_count} employee(s) ({low_att_pct:.1f}% of workforce) have attendance below the {threshold:.0f}% benchmark "
                f"({emp_names}{suffix}). Employees below the attendance threshold should be reviewed by management."
            ),
        })
    else:
        insights.append({
            "category": "Attendance Threshold",
            "type": "success",
            "title": "All Employees Meet Minimum Benchmark",
            "message": f"All {total_employees} employees have maintained attendance at or above the designated {threshold:.0f}% threshold.",
        })

    # 3. Departmental Variance Analysis
    dept_summary = get_department_summary(df)
    if not dept_summary.empty and len(dept_summary) > 1:
        highest_dept, lowest_dept = get_department_extremes(dept_summary)
        dept_gap = highest_dept["Average_Attendance_Pct"] - lowest_dept["Average_Attendance_Pct"]

        if dept_gap >= 12.0:
            insights.append({
                "category": "Department Variance",
                "type": "warning",
                "title": "High Departmental Disparity Detected",
                "message": (
                    f"A significant disparity of {dept_gap:.2f}% exists between {highest_dept['Department']} "
                    f"({highest_dept['Average_Attendance_Pct']}%) and {lowest_dept['Department']} "
                    f"({lowest_dept['Average_Attendance_Pct']}%). The {lowest_dept['Department']} department "
                    f"may require targeted attendance monitoring and workflow review."
                ),
            })
        else:
            insights.append({
                "category": "Department Variance",
                "type": "info",
                "title": "Consistent Cross-Department Attendance",
                "message": (
                    f"Attendance remains relatively uniform across departments, led by {highest_dept['Department']} "
                    f"at {highest_dept['Average_Attendance_Pct']}% and anchored by {lowest_dept['Department']} "
                    f"at {lowest_dept['Average_Attendance_Pct']}% (gap: {dept_gap:.2f}%)."
                ),
            })

    # 4. Absence vs Leave Dynamics
    if absence_rate > leave_rate:
        insights.append({
            "category": "Absence Pattern",
            "type": "warning",
            "title": "Unplanned Absences Exceed Approved Leaves",
            "message": (
                f"Overall absence rate ({absence_rate:.2f}%) exceeds the planned leave rate ({leave_rate:.2f}%). "
                "Encouraging timely leave scheduling can help minimize unexpected operational disruptions."
            ),
        })
    else:
        insights.append({
            "category": "Absence Pattern",
            "type": "info",
            "title": "Balanced Leave Planning",
            "message": (
                f"Planned leaves ({leave_rate:.2f}%) account for the majority of non-working days relative to "
                f"unplanned absences ({absence_rate:.2f}%), reflecting structured leave management."
            ),
        })

    # 5. High Performer Recognition
    perfect_attendance = df[df[COL_ATTENDANCE_PCT] == 100.0]
    if not perfect_attendance.empty:
        perf_count = len(perfect_attendance)
        perf_names = ", ".join(perfect_attendance[COL_NAME].head(3).tolist())
        perf_suffix = f" and {perf_count - 3} others" if perf_count > 3 else ""
        insights.append({
            "category": "Recognition",
            "type": "success",
            "title": "Perfect Attendance Achievers",
            "message": f"{perf_count} employee(s) achieved a 100% attendance record ({perf_names}{perf_suffix}).",
        })

    return insights
