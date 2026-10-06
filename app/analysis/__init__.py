"""Analysis package exposing attendance, department, leave, and insight modules."""

from app.analysis.attendance import (
    calculate_attendance_percentage,
    calculate_average_attendance,
    get_highest_attendance_employee,
    get_lowest_attendance_employee,
    get_low_attendance_employees,
    get_high_attendance_employees,
    calculate_present_rate,
    calculate_absence_rate,
    calculate_leave_rate,
    get_attendance_summary_metrics,
)
from app.analysis.department import (
    get_department_summary,
    get_department_extremes,
    get_department_leave_extremes,
    get_employees_in_department,
)
from app.analysis.leave import (
    calculate_leave_summary,
    get_employees_by_leave_bracket,
)
from app.analysis.insights import (
    generate_workforce_insights,
)

__all__ = [
    "calculate_attendance_percentage",
    "calculate_average_attendance",
    "get_highest_attendance_employee",
    "get_lowest_attendance_employee",
    "get_low_attendance_employees",
    "get_high_attendance_employees",
    "calculate_present_rate",
    "calculate_absence_rate",
    "calculate_leave_rate",
    "get_attendance_summary_metrics",
    "get_department_summary",
    "get_department_extremes",
    "get_department_leave_extremes",
    "get_employees_in_department",
    "calculate_leave_summary",
    "get_employees_by_leave_bracket",
    "generate_workforce_insights",
]
