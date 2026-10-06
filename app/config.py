"""Application configuration and constants."""

from pathlib import Path

# Application Metadata
APP_TITLE = "Employee Attendance Analysis & Workforce Insights System"
APP_SUBTITLE = "Data-Driven Employee Attendance Monitoring and Workforce Analytics"
APP_ICON = "📊"
APP_VERSION = "1.0.0"

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DEFAULT_DATA_PATH = DATA_DIR / "employee_attendance.csv"
SAMPLE_DATA_PATH = DATA_DIR / "sample_employee_attendance.csv"

# Column Definitions
COL_EMP_ID = "Employee_ID"
COL_NAME = "Name"
COL_DEPT = "Department"
COL_WORKING_DAYS = "Working_Days"
COL_PRESENT_DAYS = "Present_Days"
COL_ABSENT_DAYS = "Absent_Days"
COL_LEAVE_DAYS = "Leave_Days"
COL_ATTENDANCE_PCT = "Attendance_Percentage"

REQUIRED_COLUMNS = [
    COL_EMP_ID,
    COL_NAME,
    COL_DEPT,
    COL_WORKING_DAYS,
    COL_PRESENT_DAYS,
    COL_ABSENT_DAYS,
    COL_LEAVE_DAYS,
]

NUMERIC_COLUMNS = [
    COL_WORKING_DAYS,
    COL_PRESENT_DAYS,
    COL_ABSENT_DAYS,
    COL_LEAVE_DAYS,
]

# Business Logic Defaults
DEFAULT_ATTENDANCE_THRESHOLD = 80.0
HIGH_ATTENDANCE_BENCHMARK = 90.0

# Navigation Pages
PAGES = [
    "Dashboard",
    "Attendance Analysis",
    "Department Analysis",
    "Leave Analysis",
    "Employee Insights",
    "Visualizations",
    "Data Explorer",
    "Report Generation",
    "About Project",
]

# Chart Theme Colors
COLOR_PRESENT = "#2E7D32"   # Green
COLOR_ABSENT = "#D32F2F"    # Red
COLOR_LEAVE = "#F57C00"     # Amber / Orange
COLOR_PRIMARY = "#1976D2"   # Blue
COLOR_ACCENT = "#7B1FA2"    # Purple
COLOR_CARD_BG = "#F8F9FA"
