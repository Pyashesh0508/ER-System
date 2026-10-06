"""Visualizations page view."""

import streamlit as st
import pandas as pd

from app.config import DEFAULT_ATTENDANCE_THRESHOLD
from app.visualization.charts import (
    chart_department_attendance,
    chart_present_absent_leave_donut,
    chart_attendance_distribution,
    chart_employee_attendance_ranking,
    chart_department_leaves_absences,
    chart_low_attendance_employees,
)
from app.ui.components import render_page_header


def render_visualizations_view(df: pd.DataFrame, threshold: float = DEFAULT_ATTENDANCE_THRESHOLD):
    """Render Visualizations gallery page showcasing all Plotly analytical charts."""
    render_page_header(
        "Interactive Workforce Visualizations",
        "Comprehensive visual analytics powered by Plotly.",
    )

    tab1, tab2, tab3 = st.tabs([
        "🏢 Department Charts",
        "👥 Employee Comparisons",
        "🥧 Time Distribution & Leaves",
    ])

    with tab1:
        st.markdown("#### 1. Department-Wise Average Attendance")
        st.plotly_chart(chart_department_attendance(df), use_container_width=True)

        st.markdown("---")
        st.markdown("#### 2. Department Leaves vs Unplanned Absences")
        st.plotly_chart(chart_department_leaves_absences(df), use_container_width=True)

    with tab2:
        st.markdown(f"#### 3. Low Attendance Focus (< {threshold:.0f}%)")
        st.plotly_chart(chart_low_attendance_employees(df, threshold=threshold), use_container_width=True)

        st.markdown("---")
        st.markdown("#### 4. Complete Employee Attendance Ranking")
        st.plotly_chart(chart_employee_attendance_ranking(df, threshold=threshold), use_container_width=True)

    with tab3:
        st.markdown("#### 5. Present vs Absent vs Leave Time Allocation")
        st.plotly_chart(chart_present_absent_leave_donut(df), use_container_width=True)

        st.markdown("---")
        st.markdown("#### 6. Workforce Attendance Distribution")
        st.plotly_chart(chart_attendance_distribution(df), use_container_width=True)
