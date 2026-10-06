"""Dashboard page view."""

import streamlit as st
import pandas as pd

from app.analysis.attendance import get_attendance_summary_metrics
from app.analysis.insights import generate_workforce_insights
from app.visualization.charts import (
    chart_department_attendance,
    chart_present_absent_leave_donut,
    chart_attendance_distribution,
)
from app.ui.components import render_page_header, render_kpi_grid, render_insight_card


def render_dashboard(df: pd.DataFrame, threshold: float = 80.0):
    """Render main executive dashboard."""
    render_page_header(
        "Executive Workforce Dashboard",
        "Key performance indicators, attendance distribution, and department analytics.",
    )

    metrics = get_attendance_summary_metrics(df)
    render_kpi_grid(metrics)

    st.markdown("---")

    # Visualizations row 1
    col_dept, col_donut = st.columns([1.2, 1.0])

    with col_dept:
        st.plotly_chart(chart_department_attendance(df), use_container_width=True)

    with col_donut:
        st.plotly_chart(chart_present_absent_leave_donut(df), use_container_width=True)

    # Visualizations row 2: Distribution and Quick Insights
    col_dist, col_ins = st.columns([1.1, 1.0])

    with col_dist:
        st.plotly_chart(chart_attendance_distribution(df), use_container_width=True)

    with col_ins:
        st.markdown("#### 🔍 Recent Workforce Insights")
        insights = generate_workforce_insights(df, threshold=threshold)
        for ins in insights[:3]:
            render_insight_card(
                category=ins["category"],
                title=ins["title"],
                message=ins["message"],
                type_str=ins["type"],
            )
        if len(insights) > 3:
            st.caption(f"Showing 3 of {len(insights)} insights. See 'Employee Insights' tab for full report.")
