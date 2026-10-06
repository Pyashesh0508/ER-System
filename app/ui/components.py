"""Reusable Streamlit UI components."""

from typing import Dict, Any, List
import streamlit as st


def render_page_header(title: str, subtitle: str = ""):
    """Render consistent page header with title and subtitle."""
    st.markdown(f"## {title}")
    if subtitle:
        st.markdown(f"<p style='color: #64748b; margin-top: -10px; margin-bottom: 20px;'>{subtitle}</p>", unsafe_allow_html=True)


def render_kpi_card(title: str, value: Any, subtext: str = "", help_text: str = ""):
    """Render a clean custom HTML KPI card."""
    help_attr = f" title='{help_text}'" if help_text else ""
    st.markdown(
        f"""
        <div class="kpi-card"{help_attr}>
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-subtext">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_grid(metrics: Dict[str, Any]):
    """Render the standard top 4 + 3 KPI metric cards."""
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        render_kpi_card(
            title="Total Employees",
            value=metrics.get("total_employees", 0),
            subtext="Active workforce records",
        )
    with col2:
        render_kpi_card(
            title="Avg Attendance",
            value=f"{metrics.get('average_attendance', 0.0):.2f}%",
            subtext="Across all departments",
        )
    with col3:
        render_kpi_card(
            title="Present Days",
            value=f"{metrics.get('total_present_days', 0):,}",
            subtext=f"{metrics.get('present_rate', 0.0):.1f}% of total days",
        )
    with col4:
        render_kpi_card(
            title="Absent Days",
            value=f"{metrics.get('total_absent_days', 0):,}",
            subtext=f"{metrics.get('absence_rate', 0.0):.1f}% unplanned rate",
        )

    col5, col6, col7 = st.columns(3)
    with col5:
        render_kpi_card(
            title="Leave Days",
            value=f"{metrics.get('total_leave_days', 0):,}",
            subtext=f"{metrics.get('leave_rate', 0.0):.1f}% planned leave rate",
        )
    with col6:
        render_kpi_card(
            title="Highest Attendance",
            value=f"{metrics.get('highest_attendance', 0.0):.1f}%",
            subtext=metrics.get("highest_employee_name", "N/A"),
        )
    with col7:
        render_kpi_card(
            title="Lowest Attendance",
            value=f"{metrics.get('lowest_attendance', 0.0):.1f}%",
            subtext=metrics.get("lowest_employee_name", "N/A"),
        )


def render_insight_card(category: str, title: str, message: str, type_str: str = "info"):
    """Render structured insight alert box."""
    badge_type = {
        "success": "badge-success",
        "warning": "badge-warning",
        "alert": "badge-danger",
        "info": "badge-info",
    }.get(type_str, "badge-info")

    st.markdown(
        f"""
        <div class="insight-card insight-{type_str}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 700; color: #1e293b; font-size: 0.95rem;">{title}</span>
                <span class="badge {badge_type}">{category.upper()}</span>
            </div>
            <div style="font-size: 0.88rem; color: #334155; line-height: 1.45;">
                {message}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
