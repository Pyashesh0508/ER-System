"""Attendance Analysis page view."""

import streamlit as st
import pandas as pd

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
from app.analysis.attendance import (
    calculate_attendance_percentage,
    calculate_average_attendance,
    get_highest_attendance_employee,
    get_lowest_attendance_employee,
    get_low_attendance_employees,
    get_high_attendance_employees,
    calculate_present_rate,
    calculate_absence_rate,
)
from app.visualization.charts import (
    chart_employee_attendance_ranking,
    chart_low_attendance_employees,
)
from app.ui.components import render_page_header, render_kpi_card


def render_attendance_view(df: pd.DataFrame, threshold: float = DEFAULT_ATTENDANCE_THRESHOLD):
    """Render Attendance Analysis page."""
    render_page_header(
        "Attendance Performance Analysis",
        "Individual attendance rates, threshold alerts, and benchmark evaluations.",
    )

    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)

    avg_att = calculate_average_attendance(df)
    present_rate = calculate_present_rate(df)
    absence_rate = calculate_absence_rate(df)

    low_emp_df = get_low_attendance_employees(df, threshold=threshold)
    high_emp_df = get_high_attendance_employees(df, benchmark=90.0)

    # Top KPI row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Average Attendance", f"{avg_att:.2f}%", "All employees")
    with col2:
        render_kpi_card("Overall Present Rate", f"{present_rate:.2f}%", "Relative to working days")
    with col3:
        render_kpi_card("Overall Absence Rate", f"{absence_rate:.2f}%", "Unplanned absences")
    with col4:
        render_kpi_card(
            f"Below {threshold:.0f}% Benchmark",
            len(low_emp_df),
            f"{(len(low_emp_df) / len(df) * 100):.1f}% of workforce",
        )

    st.markdown("---")

    # Threshold alerting section
    st.markdown(f"### ⚠️ Low Attendance Monitoring (Threshold: {threshold:.0f}%)")
    st.caption(
        f"Employees with attendance strictly below {threshold:.0f}% are flagged for supervisory review."
    )

    if not low_emp_df.empty:
        col_table, col_chart = st.columns([1.1, 1.2])

        with col_table:
            st.markdown(f"**Identified Employees ({len(low_emp_df)} Total)**")
            display_cols = [
                COL_EMP_ID,
                COL_NAME,
                COL_DEPT,
                COL_PRESENT_DAYS,
                COL_WORKING_DAYS,
                COL_ATTENDANCE_PCT,
            ]
            st.dataframe(
                low_emp_df[display_cols].style.format({
                    COL_ATTENDANCE_PCT: "{:.2f}%",
                    COL_PRESENT_DAYS: "{:.0f}",
                    COL_WORKING_DAYS: "{:.0f}",
                }).applymap(
                    lambda v: "background-color: #fee2e2; color: #991b1b; font-weight: bold;",
                    subset=[COL_ATTENDANCE_PCT],
                ),
                use_container_width=True,
                hide_index=True,
            )

        with col_chart:
            st.plotly_chart(chart_low_attendance_employees(df, threshold=threshold), use_container_width=True)
    else:
        st.success(f"🎉 Excellent! No employees are currently below the {threshold:.0f}% attendance threshold.")

    st.markdown("---")

    # High Achievers & Overall Ranking
    tab1, tab2 = st.tabs(["📊 Complete Employee Attendance Ranking", "⭐ High Attendance Achievers (≥ 90%)"])

    with tab1:
        st.plotly_chart(
            chart_employee_attendance_ranking(df, threshold=threshold),
            use_container_width=True,
        )

    with tab2:
        st.markdown(f"**Employees Meeting or Exceeding 90% Benchmark ({len(high_emp_df)} Total)**")
        display_high = [
            COL_EMP_ID,
            COL_NAME,
            COL_DEPT,
            COL_PRESENT_DAYS,
            COL_WORKING_DAYS,
            COL_ATTENDANCE_PCT,
        ]
        st.dataframe(
            high_emp_df[display_high].style.format({
                COL_ATTENDANCE_PCT: "{:.2f}%",
                COL_PRESENT_DAYS: "{:.0f}",
                COL_WORKING_DAYS: "{:.0f}",
            }).applymap(
                lambda v: "background-color: #dcfce7; color: #166534; font-weight: bold;",
                subset=[COL_ATTENDANCE_PCT],
            ),
            use_container_width=True,
            hide_index=True,
        )
