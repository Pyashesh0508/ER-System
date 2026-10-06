"""About Project page view and College Viva demonstration guide."""

import streamlit as st

from app.config import APP_TITLE, APP_SUBTITLE, APP_VERSION
from app.ui.components import render_page_header


def render_about_view():
    """Render About Project page with Viva demonstration answers and system architecture."""
    render_page_header(
        "About the Project",
        "Academic overview, architecture, and Project-Based Learning (PBL) Viva preparation.",
    )

    st.markdown(
        f"""
        ### 🎯 {APP_TITLE} (v{APP_VERSION})
        *{APP_SUBTITLE}*

        ---
        """
    )

    st.markdown("### 🎓 PBL Viva Voce & Demonstration Guide")
    st.caption("Common questions and model answers designed to help college students explain the project during evaluation:")

    with st.expander("1. What problem does this application solve?", expanded=True):
        st.markdown(
            """
            Manual attendance tracking across organizational departments often results in delayed identification 
            of absenteeism, lack of visibility into departmental trends, and tedious manual report generation. 
            This system automates attendance rate computation, detects high-risk absenteeism using dynamic thresholds, 
            and delivers actionable workforce insights and exportable reports.
            """
        )

    with st.expander("2. What dataset structure is used?"):
        st.markdown(
            """
            The dataset is a standard CSV file containing employee attendance logs:
            - **Employee_ID**: Unique identifier for each worker.
            - **Name**: Employee full name (loaded dynamically, never hard-coded).
            - **Department**: Organizational division (e.g., Engineering, Sales, HR).
            - **Working_Days**: Total operational business days in the reporting cycle.
            - **Present_Days**: Number of days employee attended work.
            - **Absent_Days**: Unplanned, unapproved missed days.
            - **Leave_Days**: Approved planned leaves.
            """
        )

    with st.expander("3. Why are Pandas and NumPy used?"):
        st.markdown(
            """
            - **Pandas**: Provides fast DataFrame operations for data ingestion, missing value sanitization, 
              filtering, sorting, and department-level group aggregation (`groupby`).
            - **NumPy**: Powers vectorized numerical calculations (`np.where`, `np.round`), ensuring 
              division-by-zero safety when calculating attendance percentages across thousands of records.
            """
        )

    with st.expander("4. Why is Plotly used instead of static charts (e.g., Matplotlib)?"):
        st.markdown(
            """
            Plotly provides browser-native interactive charts that support zooming, panning, interactive hover tooltips, 
            and responsive resizing directly within the Streamlit dashboard, enhancing user experience compared to 
            static raster image charts.
            """
        )

    with st.expander("5. How is Attendance Percentage mathematically calculated?"):
        st.latex(r"\text{Attendance Percentage} = \left(\frac{\text{Present Days}}{\text{Working Days}}\right) \times 100")
        st.markdown("The final percentage is rounded to two decimal places for business precision.")

    with st.expander("6. How does department analysis work?"):
        st.markdown(
            """
            The records are grouped by `Department` using Pandas aggregation. The application computes:
            - Headcount per department
            - Department-wide average attendance %
            - Aggregate and average present, absent, and leave days
            - Disparities between top-performing and under-performing divisions.
            """
        )

    with st.expander("7. How are low-attendance employees flagged?"):
        st.markdown(
            """
            The system applies a configurable attendance threshold filter (default **80%**). Any employee whose 
            attendance percentage is strictly lower than this benchmark is tagged, tabulated, and surfaced in the 
            managerial review alerts.
            """
        )

    with st.expander("8. How are automated reports generated?"):
        st.markdown(
            """
            - **PDF Reports**: Generated programmatically using `ReportLab`, combining executive KPI tables, 
              department summaries, and dynamic two-pass page numbering (`NumberedCanvas`).
            - **Excel Workbooks**: Created via `openpyxl`, organizing data across three styled sheets 
              (*Employee Data*, *Department Summary*, *Workforce Insights*).
            """
        )

    with st.expander("9. How is data privacy maintained?"):
        st.markdown(
            """
            All data processing, analytics, and file exports are executed 100% locally on the host machine. 
            No employee data is transmitted over external networks or third-party cloud APIs.
            """
        )

    st.markdown("---")
    st.markdown("### 🛠️ Technology Stack")
    st.markdown(
        """
        | Component | Technology | Role |
        |---|---|---|
        | Web Dashboard | **Streamlit** | Interactive UI and routing |
        | Data Processing | **Pandas** | Tabular data manipulation and grouping |
        | Calculations | **NumPy** | High-performance vectorized arithmetic |
        | Interactive Visuals | **Plotly** | Responsive charts and graphs |
        | PDF Generator | **ReportLab** | Enterprise PDF document creation |
        | Excel Generator | **openpyxl** | Multi-sheet formatted spreadsheet export |
        | Testing Suite | **pytest** | Unit and functional test validation |
        """
    )
