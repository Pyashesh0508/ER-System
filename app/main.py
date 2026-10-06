"""Main application entrypoint for Streamlit."""

import sys
from pathlib import Path

# Add project root to path for reliable module resolution
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
import pandas as pd

from app.config import (
    APP_TITLE,
    APP_SUBTITLE,
    APP_ICON,
    DEFAULT_DATA_PATH,
    SAMPLE_DATA_PATH,
    DEFAULT_ATTENDANCE_THRESHOLD,
    PAGES,
)
from app.data.loader import load_attendance_data, load_csv_from_upload
from app.data.validator import validate_attendance_dataframe
from app.analysis.attendance import calculate_attendance_percentage
from app.ui.styles import CUSTOM_CSS
from app.ui import (
    render_dashboard,
    render_attendance_view,
    render_department_view,
    render_leave_view,
    render_insights_view,
    render_visualizations_view,
    render_explorer_view,
    render_reports_view,
    render_about_view,
)


def init_session_state():
    """Initialize session state variables."""
    if "attendance_threshold" not in st.session_state:
        st.session_state["attendance_threshold"] = DEFAULT_ATTENDANCE_THRESHOLD
    if "data_source_name" not in st.session_state:
        st.session_state["data_source_name"] = "Default Dataset"


def main():
    """Main application orchestrator."""
    st.set_page_config(
        page_title="Workforce Attendance Analytics",
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Inject custom UI styles
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
    init_session_state()

    # Sidebar Header
    st.sidebar.markdown(f"### {APP_ICON} Workforce Insights")
    st.sidebar.caption(APP_SUBTITLE)
    st.sidebar.markdown("---")

    # Data Source Selection & File Uploader
    st.sidebar.markdown("#### 📂 Data Management")
    uploaded_file = st.sidebar.file_uploader(
        "Upload Employee Attendance CSV:",
        type=["csv"],
        help="Upload your own custom attendance CSV file.",
    )

    use_sample = st.sidebar.checkbox(
        "Use Sample Dataset",
        value=False,
        help="Toggle to load sample_employee_attendance.csv instead.",
    )

    # Load appropriate dataset
    raw_df = None
    load_error = None
    source_name = "Default Dataset"

    if uploaded_file is not None:
        raw_df, load_error = load_csv_from_upload(uploaded_file)
        source_name = f"Uploaded: {uploaded_file.name}"
    elif use_sample:
        raw_df, load_error = load_attendance_data(SAMPLE_DATA_PATH)
        source_name = "Sample Dataset (10 records)"
    else:
        raw_df, load_error = load_attendance_data(DEFAULT_DATA_PATH)
        source_name = "Default Dataset (data/employee_attendance.csv)"

    st.session_state["data_source_name"] = source_name

    # Handle file reading errors gracefully
    if load_error or raw_df is None:
        st.sidebar.error("❌ Data loading failed.")
        st.error(f"### ⚠️ Data Loading Error\n\n{load_error}")
        st.info(
            "Please check that `data/employee_attendance.csv` exists, or upload a valid CSV file using the sidebar."
        )
        return

    # Validate DataFrame
    validation_res = validate_attendance_dataframe(raw_df)

    if not validation_res.is_valid:
        st.sidebar.error("❌ Data validation failed.")
        st.error("### ⚠️ Dataset Validation Issues Detected")
        st.markdown(
            "The loaded dataset contains logical or formatting inconsistencies that prevent accurate analysis:"
        )
        for err in validation_res.errors:
            st.markdown(f"- ❌ **{err}**")

        st.warning(
            "**Required CSV Column Headers:**\n\n"
            "`Employee_ID`, `Name`, `Department`, `Working_Days`, `Present_Days`, `Absent_Days`, `Leave_Days`\n\n"
            "Please correct the CSV file and re-upload."
        )
        return

    # Work with cleaned and enriched DataFrame
    df = validation_res.cleaned_df
    df = calculate_attendance_percentage(df)

    # Show dataset status in sidebar
    st.sidebar.success(f"✓ Loaded {len(df)} employee records")
    st.sidebar.caption(f"Source: *{source_name}*")

    if validation_res.has_warnings:
        with st.sidebar.expander("⚠️ Data Warnings", expanded=False):
            for warn in validation_res.warnings:
                st.caption(f"• {warn}")

    st.sidebar.markdown("---")

    # Global Settings
    st.sidebar.markdown("#### ⚙️ Configuration")
    threshold = st.sidebar.slider(
        "Attendance Threshold (%):",
        min_value=50.0,
        max_value=95.0,
        value=float(st.session_state.get("attendance_threshold", DEFAULT_ATTENDANCE_THRESHOLD)),
        step=1.0,
        help="Employees below this percentage will be flagged for review.",
    )
    st.session_state["attendance_threshold"] = threshold

    st.sidebar.markdown("---")

    # Sidebar Page Navigation
    st.sidebar.markdown("#### 🧭 Navigation")
    selected_page = st.sidebar.radio(
        "Go to page:",
        options=PAGES,
        index=0,
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Employee Attendance Analytics v1.0.0\nPBL Micro Project")

    # Route to Selected Page with Error Handling
    try:
        if selected_page == "Dashboard":
            render_dashboard(df, threshold=threshold)
        elif selected_page == "Attendance Analysis":
            render_attendance_view(df, threshold=threshold)
        elif selected_page == "Department Analysis":
            render_department_view(df)
        elif selected_page == "Leave Analysis":
            render_leave_view(df)
        elif selected_page == "Employee Insights":
            render_insights_view(df, threshold=threshold)
        elif selected_page == "Visualizations":
            render_visualizations_view(df, threshold=threshold)
        elif selected_page == "Data Explorer":
            render_explorer_view(df)
        elif selected_page == "Report Generation":
            render_reports_view(df, threshold=threshold)
        elif selected_page == "About Project":
            render_about_view()
    except Exception as e:
        st.error(f"An unexpected error occurred while rendering the page: {str(e)}")
        st.info("Try refreshing the page or switching to the Dashboard.")


if __name__ == "__main__":
    main()
