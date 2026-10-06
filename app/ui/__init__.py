"""UI package exposing styles, components, and views."""

from app.ui.styles import CUSTOM_CSS
from app.ui.components import render_page_header, render_kpi_card, render_kpi_grid, render_insight_card
from app.ui.dashboard import render_dashboard
from app.ui.attendance_view import render_attendance_view
from app.ui.department_view import render_department_view
from app.ui.leave_view import render_leave_view
from app.ui.insights_view import render_insights_view
from app.ui.visualizations_view import render_visualizations_view
from app.ui.explorer_view import render_explorer_view
from app.ui.reports_view import render_reports_view
from app.ui.about_view import render_about_view

__all__ = [
    "CUSTOM_CSS",
    "render_page_header",
    "render_kpi_card",
    "render_kpi_grid",
    "render_insight_card",
    "render_dashboard",
    "render_attendance_view",
    "render_department_view",
    "render_leave_view",
    "render_insights_view",
    "render_visualizations_view",
    "render_explorer_view",
    "render_reports_view",
    "render_about_view",
]
