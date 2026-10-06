"""Leave Analysis page view."""

import streamlit as st
import pandas as pd
import plotly.express as px

from app.config import (
    COL_EMP_ID,
    COL_NAME,
    COL_DEPT,
    COL_LEAVE_DAYS,
    COL_ATTENDANCE_PCT,
    COLOR_LEAVE,
)
from app.analysis.leave import (
    calculate_leave_summary,
    get_employees_by_leave_bracket,
)
from app.ui.components import render_page_header, render_kpi_card


def render_leave_view(df: pd.DataFrame):
    """Render Leave Analysis page."""
    render_page_header(
        "Employee Leave Pattern Analysis",
        "Planned leaves, allocation across departments, and frequency distribution.",
    )

    # Department filter selection
    dept_options = ["All"] + sorted(df[COL_DEPT].dropna().unique().tolist())
    selected_dept = st.selectbox("Filter analysis by department:", dept_options, index=0)

    summary = calculate_leave_summary(df, department_filter=selected_dept)

    # Top KPI metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card("Total Leave Days", f"{summary['total_leave_days']:,}", f"Scope: {selected_dept}")
    with col2:
        render_kpi_card("Avg Leave / Person", f"{summary['avg_leave_per_employee']:.2f} days", "Department average" if selected_dept != "All" else "Overall average")
    with col3:
        render_kpi_card("Max Leave Days", f"{summary['max_leave_days']} days", f"Taken by: {summary['top_leave_employees']}")
    with col4:
        render_kpi_card("Min Leave Days", f"{summary['min_leave_days']} days", "Minimum recorded")

    st.markdown("---")

    # Leave distribution & brackets
    filtered_df = df if selected_dept == "All" else df[df[COL_DEPT] == selected_dept]
    bracket_df = get_employees_by_leave_bracket(filtered_df)

    col_chart, col_dept_ext = st.columns([1.2, 1.0])

    with col_chart:
        st.markdown("#### 📊 Leave Days Bracket Distribution")
        bracket_counts = bracket_df["Leave_Bracket"].value_counts().reset_index()
        bracket_counts.columns = ["Bracket", "Employee_Count"]

        fig_bracket = px.bar(
            bracket_counts,
            x="Bracket",
            y="Employee_Count",
            text="Employee_Count",
            color_discrete_sequence=[COLOR_LEAVE],
            labels={"Bracket": "Leave Range", "Employee_Count": "Employees"},
            title="Workforce Split by Leave Days Taken",
        )
        fig_bracket.update_traces(textposition="outside")
        fig_bracket.update_layout(template="plotly_white", height=350)
        st.plotly_chart(fig_bracket, use_container_width=True)

    with col_dept_ext:
        st.markdown("#### 🏢 Department Leave Benchmarks")
        st.info(f"**Highest Leave Department:**\n\n{summary['department_highest_leave']}")
        st.success(f"**Lowest Leave Department:**\n\n{summary['department_lowest_leave']}")

        st.caption(
            "Balanced leave taking promotes employee well-being while avoiding sudden workforce deficits."
        )

    st.markdown("---")

    # Employee Leave Records Table
    st.markdown("### 📋 Employee Leave Records")
    display_cols = [COL_EMP_ID, COL_NAME, COL_DEPT, COL_LEAVE_DAYS, "Absent_Days", COL_ATTENDANCE_PCT]
    st.dataframe(
        filtered_df[display_cols].sort_values(by=COL_LEAVE_DAYS, ascending=False).style.format({
            COL_ATTENDANCE_PCT: "{:.2f}%",
            COL_LEAVE_DAYS: "{:.0f}",
            "Absent_Days": "{:.0f}",
        }),
        use_container_width=True,
        hide_index=True,
    )
