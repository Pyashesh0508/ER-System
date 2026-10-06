"""Department Analysis page view."""

import streamlit as st
import pandas as pd

from app.config import (
    COL_EMP_ID,
    COL_NAME,
    COL_DEPT,
    COL_PRESENT_DAYS,
    COL_WORKING_DAYS,
    COL_ATTENDANCE_PCT,
)
from app.analysis.department import (
    get_department_summary,
    get_department_extremes,
    get_department_leave_extremes,
    get_employees_in_department,
)
from app.visualization.charts import (
    chart_department_attendance,
    chart_department_leaves_absences,
)
from app.ui.components import render_page_header, render_kpi_card


def render_department_view(df: pd.DataFrame):
    """Render Department Analysis page."""
    render_page_header(
        "Department-Wise Attendance Analysis",
        "Comparative metrics, organizational breakdown, and departmental trends.",
    )

    dept_summary = get_department_summary(df)
    if dept_summary.empty:
        st.warning("No department data available to analyze.")
        return

    highest_dept, lowest_dept = get_department_extremes(dept_summary)
    high_leave_dept, low_leave_dept = get_department_leave_extremes(dept_summary)

    # Department highlights row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card(
            "Top Department",
            f"{highest_dept.get('Average_Attendance_Pct', 0):.1f}%",
            highest_dept.get("Department", "N/A"),
        )
    with col2:
        render_kpi_card(
            "Lowest Department",
            f"{lowest_dept.get('Average_Attendance_Pct', 0):.1f}%",
            lowest_dept.get("Department", "N/A"),
        )
    with col3:
        render_kpi_card(
            "Highest Avg Leave",
            f"{high_leave_dept.get('Avg_Leave_Days', 0):.1f} days",
            high_leave_dept.get("Department", "N/A"),
        )
    with col4:
        render_kpi_card(
            "Lowest Avg Leave",
            f"{low_leave_dept.get('Avg_Leave_Days', 0):.1f} days",
            low_leave_dept.get("Department", "N/A"),
        )

    st.markdown("---")

    # Visualizations Row
    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.plotly_chart(chart_department_attendance(df), use_container_width=True)
    with col_chart2:
        st.plotly_chart(chart_department_leaves_absences(df), use_container_width=True)

    # Department Data Table
    st.markdown("### 📋 Department Aggregate Summary Table")
    st.dataframe(
        dept_summary.style.format({
            "Average_Attendance_Pct": "{:.2f}%",
            "Avg_Present_Days": "{:.2f}",
            "Avg_Absent_Days": "{:.2f}",
            "Avg_Leave_Days": "{:.2f}",
            "Employee_Count": "{:.0f}",
            "Total_Working_Days": "{:.0f}",
            "Total_Present_Days": "{:.0f}",
            "Total_Absent_Days": "{:.0f}",
            "Total_Leave_Days": "{:.0f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    # Department Drill-Down
    st.markdown("### 🔍 Department Member Drill-Down")
    dept_list = sorted(df[COL_DEPT].dropna().unique().tolist())
    selected_dept = st.selectbox("Select Department to inspect member records:", dept_list)

    if selected_dept:
        members_df = get_employees_in_department(df, selected_dept)
        st.caption(f"Showing {len(members_df)} employees in **{selected_dept}**:")
        st.dataframe(
            members_df[[COL_EMP_ID, COL_NAME, COL_WORKING_DAYS, COL_PRESENT_DAYS, "Absent_Days", "Leave_Days", COL_ATTENDANCE_PCT]]
            .style.format({COL_ATTENDANCE_PCT: "{:.2f}%"}),
            use_container_width=True,
            hide_index=True,
        )
