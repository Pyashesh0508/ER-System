"""Report Generation and Data Export page view."""

import streamlit as st
import pandas as pd
from datetime import datetime

from app.analysis.attendance import calculate_attendance_percentage
from app.reports.pdf_report import generate_pdf_report
from app.reports.excel_report import generate_excel_report
from app.ui.components import render_page_header


def render_reports_view(df: pd.DataFrame, threshold: float = 80.0):
    """Render Report Generation page."""
    render_page_header(
        "Report Generation & Data Export",
        "Generate and download publication-ready PDF reports, formatted Excel workbooks, and CSVs.",
    )

    if COL_ATTENDANCE_PCT := "Attendance_Percentage":
        if COL_ATTENDANCE_PCT not in df.columns:
            df = calculate_attendance_percentage(df)

    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M")

    col_pdf, col_excel, col_csv = st.columns(3)

    # 1. PDF Report Card
    with col_pdf:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-title">Executive Document</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #1e293b; margin: 6px 0;">
                    📄 PDF Report
                </div>
                <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 12px; line-height: 1.4;">
                    Formal multi-page report containing executive KPIs, department breakdowns, threshold review, and observations.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            with st.spinner("Generating PDF report..."):
                pdf_bytes = generate_pdf_report(df, threshold=threshold)
            st.download_button(
                label="📥 Download PDF Report",
                data=pdf_bytes,
                file_name=f"Workforce_Attendance_Report_{timestamp_str}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Unable to generate PDF report: {str(e)}")

    # 2. Excel Report Card
    with col_excel:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-title">Multi-Tab Workbook</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #1e293b; margin: 6px 0;">
                    📊 Excel Workbook
                </div>
                <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 12px; line-height: 1.4;">
                    Styled spreadsheet (.xlsx) with 3 sheets: Employee Data, Department Summary, and Workforce Insights.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        try:
            with st.spinner("Preparing Excel workbook..."):
                excel_bytes = generate_excel_report(df, threshold=threshold)
            st.download_button(
                label="📥 Download Excel Workbook",
                data=excel_bytes,
                file_name=f"Workforce_Attendance_Analytics_{timestamp_str}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"Unable to generate Excel report: {str(e)}")

    # 3. CSV Export Card
    with col_csv:
        st.markdown(
            """
            <div class="kpi-card">
                <div class="kpi-title">Raw Data Export</div>
                <div style="font-size: 1.25rem; font-weight: 700; color: #1e293b; margin: 6px 0;">
                    📑 Analyzed CSV
                </div>
                <div style="font-size: 0.85rem; color: #64748b; margin-bottom: 12px; line-height: 1.4;">
                    Standard CSV file including all original columns plus the calculated <code>Attendance_Percentage</code>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Analyzed CSV",
            data=csv_bytes,
            file_name=f"Analyzed_Employee_Attendance_{timestamp_str}.csv",
            mime="text/csv",
            use_container_width=True,
        )

    st.markdown("---")

    # Preview of Included Tables
    st.markdown("### 🔍 Dataset Summary to be Exported")
    st.dataframe(
        df.head(10).style.format({
            "Attendance_Percentage": "{:.2f}%",
            "Working_Days": "{:.0f}",
            "Present_Days": "{:.0f}",
            "Absent_Days": "{:.0f}",
            "Leave_Days": "{:.0f}",
        }),
        use_container_width=True,
        hide_index=True,
    )
    st.caption(f"Showing first 10 rows of {len(df)} total records ready for export.")
