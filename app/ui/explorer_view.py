"""Data Explorer and Employee Search page view."""

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
)
from app.analysis.attendance import calculate_attendance_percentage
from app.visualization.charts import chart_single_employee_breakdown
from app.ui.components import render_page_header, render_kpi_card


def render_explorer_view(df: pd.DataFrame):
    """Render Data Explorer and Individual Employee Search view."""
    render_page_header(
        "Data Explorer & Employee Lookup",
        "Interactive filtering, multi-criteria search, and individual employee profile cards.",
    )

    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)

    tab_explore, tab_search = st.tabs(["🔎 Multi-Criteria Data Explorer", "👤 Single Employee Lookup"])

    with tab_explore:
        # Filter controls
        col_search, col_dept = st.columns([1.2, 1.2])

        with col_search:
            search_query = st.text_input("Search by Employee Name:", placeholder="e.g. Aarav, Priya...").strip().lower()

        with col_dept:
            all_depts = sorted(df[COL_DEPT].dropna().unique().tolist())
            selected_depts = st.multiselect("Filter by Department:", options=all_depts, default=[])

        col_range_att, col_range_leave = st.columns(2)

        min_att = float(df[COL_ATTENDANCE_PCT].min())
        max_att = float(df[COL_ATTENDANCE_PCT].max())
        with col_range_att:
            att_range = st.slider(
                "Filter by Attendance % Range:",
                min_value=0.0,
                max_value=100.0,
                value=(min_att, max_att),
                step=1.0,
            )

        max_leave_val = int(df[COL_LEAVE_DAYS].max()) if not df.empty else 10
        with col_range_leave:
            leave_range = st.slider(
                "Filter by Leave Days:",
                min_value=0,
                max_value=max(max_leave_val, 1),
                value=(0, max(max_leave_val, 1)),
                step=1,
            )

        # Apply filters
        filtered_df = df.copy()

        if search_query:
            filtered_df = filtered_df[filtered_df[COL_NAME].str.lower().str.contains(search_query)]

        if selected_depts:
            filtered_df = filtered_df[filtered_df[COL_DEPT].isin(selected_depts)]

        filtered_df = filtered_df[
            (filtered_df[COL_ATTENDANCE_PCT] >= att_range[0])
            & (filtered_df[COL_ATTENDANCE_PCT] <= att_range[1])
            & (filtered_df[COL_LEAVE_DAYS] >= leave_range[0])
            & (filtered_df[COL_LEAVE_DAYS] <= leave_range[1])
        ]

        st.caption(f"Showing **{len(filtered_df)}** of **{len(df)}** employees matching active filters.")

        st.dataframe(
            filtered_df.style.format({
                COL_ATTENDANCE_PCT: "{:.2f}%",
                COL_PRESENT_DAYS: "{:.0f}",
                COL_WORKING_DAYS: "{:.0f}",
                COL_ABSENT_DAYS: "{:.0f}",
                COL_LEAVE_DAYS: "{:.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )

        # CSV Download for filtered data
        csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv_bytes,
            file_name="filtered_employee_attendance.csv",
            mime="text/csv",
        )

    with tab_search:
        st.markdown("### Select an Employee to view comprehensive profile:")

        emp_options = df.apply(
            lambda row: f"{row[COL_EMP_ID]} - {row[COL_NAME]} ({row[COL_DEPT]})", axis=1
        ).tolist()

        selected_label = st.selectbox("Choose Employee:", options=emp_options)

        if selected_label:
            emp_id = selected_label.split(" - ")[0].strip()
            emp_row = df[df[COL_EMP_ID] == emp_id].iloc[0]

            col_info, col_breakdown = st.columns([1.1, 1.2])

            with col_info:
                st.markdown(f"#### Profile: **{emp_row[COL_NAME]}**")
                st.markdown(f"**ID:** `{emp_row[COL_EMP_ID]}` | **Department:** `{emp_row[COL_DEPT]}`")

                c1, c2 = st.columns(2)
                with c1:
                    render_kpi_card("Working Days", int(emp_row[COL_WORKING_DAYS]), "Scheduled")
                    render_kpi_card("Absent Days", int(emp_row[COL_ABSENT_DAYS]), "Unplanned")
                with c2:
                    render_kpi_card("Present Days", int(emp_row[COL_PRESENT_DAYS]), f"{emp_row[COL_ATTENDANCE_PCT]:.1f}% Rate")
                    render_kpi_card("Leave Days", int(emp_row[COL_LEAVE_DAYS]), "Approved")

            with col_breakdown:
                st.plotly_chart(chart_single_employee_breakdown(emp_row), use_container_width=True)
