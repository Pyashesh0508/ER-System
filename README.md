# Employee Attendance Analysis & Workforce Insights System

> **Data-Driven Employee Attendance Monitoring and Workforce Analytics**  
> *A modular, professional Project-Based Learning (PBL) micro project developed in Python & Streamlit.*

---

## 📌 Project Overview & Problem Statement

In organizational workforce management, monitoring employee attendance is critical for operational efficiency, workload balancing, and proactive human resource management. Traditional attendance management systems often rely on static spreadsheets or isolated punch-clock databases, presenting several limitations:
- **Delayed Intervention:** Inability to immediately detect chronic absenteeism or sudden dips below organizational compliance thresholds.
- **Departmental Blindspots:** Lack of cross-departmental comparative metrics to determine whether absenteeism is localized or systemic.
- **Manual Overhead:** Time-consuming manual report compilation and absence-rate calculations.

### Objective
The **Employee Attendance Analysis & Workforce Insights System** automates the entire analytical lifecycle:
1. Dynamic ingestion and validation of employee attendance CSV records (without hard-coded employee names).
2. Exact calculation of attendance percentages using standardized business logic.
3. Department-level aggregation and comparative disparity tracking.
4. Leave vs. unplanned absence trend identification.
5. Dynamic threshold-based alerting (< 80% default benchmark).
6. Automated generation of executive-grade PDF reports (ReportLab) and multi-sheet Excel workbooks (openpyxl).
7. Interactive data exploration, multi-criteria filtering, and employee profile lookup.

---

## 🚀 Key Features

| Feature | Description |
|---|---|
| **Executive Dashboard** | 7 top-level KPI cards (Total Employees, Avg Attendance, Present Days, Absent Days, Leave Days, Extremes) and summary visualizations. |
| **Attendance Analysis** | Exact formula computation, configurable benchmark threshold, and flagged list of employees requiring supervisory review. |
| **Department Analytics** | Multi-department headcount, average attendance, leave metrics, and member drill-down inspection. |
| **Leave Pattern Tracking** | Classification into leave brackets (0 days, 1-2 days, 3-4 days, 5+ days) and planned leaves vs unplanned absence comparisons. |
| **Workforce Insights** | Deterministic, rule-based analytical observations highlighting organizational health and operational risk areas. |
| **Interactive Visualizations** | Plotly-powered charts (bar charts, time allocation donut, distribution histogram, employee rankings). |
| **Data Explorer & Search** | Multi-criteria search by employee name, department multi-select, attendance range slider, leave days range, and instant CSV export. |
| **Single Employee Lookup** | Detailed personal attendance profile card with individual day breakdown donut chart. |
| **Publication-Grade Reports** | Single-click export of structured **PDF reports** (with dynamic two-pass page numbering) and **Excel workbooks** (3 styled sheets). |
| **Graceful Data Validation** | Dedicated validator detecting missing headers, negative values, and inconsistencies without crashing the UI. |

---

## 🛠️ Technology Stack

- **Application & Dashboard Framework:** [Streamlit](https://streamlit.io/) (v1.30+)
- **Data Manipulation & Ingestion:** [Pandas](https://pandas.pydata.org/) (v2.0+)
- **Vectorized Numerical Computing:** [NumPy](https://numpy.org/) (v1.24+)
- **Interactive Visualizations:** [Plotly](https://plotly.com/python/) (v5.18+)
- **PDF Generation:** [ReportLab](https://www.reportlab.com/) (v4.0+)
- **Excel Generation:** [openpyxl](https://openpyxl.readthedocs.io/) (v3.1+)
- **Automated Testing Suite:** [pytest](https://docs.pytest.org/) (v7.4+)
- **No Notebook / Anaconda Dependency:** Runs directly via standard Python virtual environment or system Python.

---

## 📂 Project Architecture

```
Project/
├── app/
│   ├── __init__.py               # App package initialization
│   ├── main.py                   # Central Streamlit app runner & router
│   ├── config.py                 # Central application settings & constants
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py             # Multi-encoding CSV reader & error handler
│   │   └── validator.py          # Data schema & relational validation
│   ├── analysis/
│   │   ├── __init__.py
│   │   ├── attendance.py         # Attendance percentage & rate formulas
│   │   ├── department.py         # Department-wise aggregations
│   │   ├── leave.py              # Leave pattern statistics
│   │   └── insights.py           # Rule-based analytical observation engine
│   ├── visualization/
│   │   ├── __init__.py
│   │   └── charts.py             # Plotly interactive chart builders
│   ├── reports/
│   │   ├── __init__.py
│   │   ├── pdf_report.py         # Publication-grade PDF generator (ReportLab)
│   │   └── excel_report.py       # Multi-sheet styled Excel generator (openpyxl)
│   └── ui/
│       ├── __init__.py
│       ├── styles.py             # Clean CSS styles for cards & badges
│       ├── components.py         # Reusable KPI cards and headers
│       ├── dashboard.py          # Executive Dashboard view
│       ├── attendance_view.py    # Attendance Analysis view
│       ├── department_view.py    # Department Analysis view
│       ├── leave_view.py         # Leave Analysis view
│       ├── insights_view.py      # Workforce Insights view
│       ├── visualizations_view.py# Visualizations Gallery view
│       ├── explorer_view.py      # Data Explorer & Lookup view
│       ├── reports_view.py       # Report Generation & Download view
│       └── about_view.py         # About Project & Viva Guide view
├── data/
│   ├── employee_attendance.csv   # Primary dataset
│   └── sample_employee_attendance.csv # Sample dataset for quick demos
├── tests/
│   ├── __init__.py
│   ├── test_loader.py            # CSV loader tests
│   ├── test_validator.py         # Data validation tests
│   ├── test_attendance.py        # Attendance formula & metric tests
│   ├── test_department.py        # Department aggregation tests
│   ├── test_leave.py             # Leave analysis tests
│   ├── test_insights.py          # Insights generation tests
│   └── test_reports.py           # PDF and Excel generation tests
├── requirements.txt              # Production dependencies
├── .gitignore                    # Python & environment gitignore
├── run_app.bat                   # 1-click launcher for Windows
├── run_app.sh                    # 1-click launcher for Linux/macOS
└── README.md                     # Documentation and Viva preparation guide
```

---

## 📊 CSV Dataset Structure

The application expects a CSV file containing the following columns:

| Column Name | Data Type | Description |
|---|---|---|
| `Employee_ID` | String | Unique employee code (e.g., `EMP001`) |
| `Name` | String | Full name (dynamically loaded; never hard-coded) |
| `Department` | String | Organizational department (e.g., `Engineering`, `Sales`) |
| `Working_Days` | Integer | Total business days in the evaluation period ($>0$) |
| `Present_Days` | Integer | Total days employee was physically/remotely present ($\ge 0$) |
| `Absent_Days` | Integer | Unplanned absence days ($\ge 0$) |
| `Leave_Days` | Integer | Approved/planned leave days ($\ge 0$) |

### Mathematical Formula

The attendance percentage for each employee is calculated as:

$$\text{Attendance Percentage} = \left(\frac{\text{Present Days}}{\text{Working Days}}\right) \times 100$$

*(Values are rounded to 2 decimal places for reporting).*

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.11+ (Python 3.11, 3.12, 3.13, 3.14 supported)
- Standard pip package manager

### 1. Clone or Open Project Directory
```powershell
cd d:\Project
```

### 2. (Optional) Create and Activate Virtual Environment
```powershell
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux / macOS:
source .venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 🏃 Running the Application

### Option A: Using Windows Launcher
Simply double-click or run:
```cmd
run_app.bat
```

### Option B: Using Linux/macOS Launcher
```bash
chmod +x run_app.sh
./run_app.sh
```

### Option C: Using Streamlit CLI Directly
```bash
streamlit run app/main.py
```

The application will start and open automatically in your browser at:
`http://localhost:8501`

---

## 🧪 Running Automated Tests

Run the full pytest suite to verify all calculations, loaders, validators, and report generators:

```powershell
python -m pytest -v
```

All 23 tests should execute and pass cleanly:
```
tests/test_attendance.py::test_attendance_percentage_exact_formula PASSED
tests/test_attendance.py::test_average_attendance PASSED
tests/test_attendance.py::test_low_attendance_filtering PASSED
tests/test_attendance.py::test_highest_and_lowest_attendance_employee PASSED
tests/test_attendance.py::test_rates_calculation PASSED
tests/test_department.py::test_department_summary_metrics PASSED
tests/test_department.py::test_department_extremes PASSED
tests/test_department.py::test_filter_employees_in_department PASSED
tests/test_insights.py::test_generate_workforce_insights_healthy PASSED
tests/test_insights.py::test_generate_workforce_insights_low_attendance_alert PASSED
tests/test_leave.py::test_leave_summary_calculations PASSED
tests/test_leave.py::test_leave_summary_with_department_filter PASSED
tests/test_leave.py::test_leave_brackets_assignment PASSED
tests/test_loader.py::test_load_default_attendance_data PASSED
tests/test_loader.py::test_load_sample_attendance_data PASSED
tests/test_loader.py::test_load_non_existent_file PASSED
tests/test_reports.py::test_pdf_report_generation PASSED
tests/test_reports.py::test_excel_report_generation PASSED
tests/test_validator.py::test_validator_valid_dataset PASSED
tests/test_validator.py::test_validator_missing_column PASSED
tests/test_validator.py::test_validator_negative_days PASSED
tests/test_validator.py::test_validator_zero_working_days PASSED
tests/test_validator.py::test_validator_present_exceeds_working PASSED
```

---

## 📖 How to Use the Application

1. **Dashboard:** Review company-wide attendance health, primary KPIs, and department attendance comparisons.
2. **Attendance Analysis:** Adjust the attendance threshold slider (e.g., 75%, 80%, 85%) to identify employees requiring management follow-up.
3. **Department Analysis:** Compare performance across departments and drill down into individual team members.
4. **Leave Analysis:** Filter leave trends by department and identify leave bracket concentrations.
5. **Employee Insights:** Review automated observations regarding organizational attendance stability and actionable recommendations.
6. **Visualizations:** View high-resolution interactive Plotly graphs with hover tooltips and responsive zoom.
7. **Data Explorer:** Use search filters (by name, department, attendance range, leave days) and download filtered sub-sets.
8. **Report Generation:** Download publication-ready PDF reports, 3-sheet Excel spreadsheets, or analyzed CSV datasets.
9. **Uploading Custom CSV:** Upload any student or company CSV directly using the sidebar file uploader; the application immediately processes new employee names and values without server restarts.

---

## 🎓 PBL Viva Voce & Demonstration Guide

If presenting this project in a college viva or evaluation, be prepared to answer:

1. **Why is this problem practically significant?**  
   *Absenteeism affects company productivity and team morale. Automating attendance rate calculation and threshold alerting gives human resource managers early warning before operational bottlenecks occur.*
2. **Why use Streamlit over a Jupyter Notebook?**  
   *A notebook is an exploratory environment requiring technical familiarity to execute cells in order. Streamlit converts Python logic into a standalone, reactive web application that non-technical managers and business stakeholders can directly use.*
3. **Why use ReportLab and openpyxl?**  
   *Business stakeholders require deliverables in standard formats. ReportLab generates formatted PDF documents with tables and headers, while openpyxl creates structured multi-tab spreadsheets with custom styling.*
4. **How are privacy and security ensured?**  
   *All computation and report rendering occur locally in Python memory. No external third-party API or cloud storage receives the employee data.*

---

## 🔮 Future Enhancements

- Multi-month trend tracking and historical month-over-month attendance comparisons.
- Biometric hardware machine integration via REST API.
- Shift scheduling and overtime / compensatory off (comp-off) tracking.
- Email dispatch integration for automated monthly PDF report delivery to department heads.

---

## 📄 License
This project is developed for educational and Project-Based Learning (PBL) demonstration purposes.
