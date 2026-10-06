"""PDF Report Generator for Employee Attendance Analysis using ReportLab."""

from datetime import datetime
from io import BytesIO
from typing import List
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)

from app.config import (
    APP_TITLE,
    APP_SUBTITLE,
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
    get_attendance_summary_metrics,
    get_low_attendance_employees,
)
from app.analysis.department import get_department_summary
from app.analysis.insights import generate_workforce_insights


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and display total page count."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))

        # Running header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, f"{APP_TITLE} — Executive Report")
            self.setStrokeColor(colors.HexColor("#CCCCCC"))
            self.setLineWidth(0.5)
            self.line(54, 750, 558, 750)

        # Running footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, page_str)
        generated_str = f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        self.drawString(54, 35, generated_str)

        self.setStrokeColor(colors.HexColor("#E0E0E0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 558, 45)
        self.restoreState()


def generate_pdf_report(
    df: pd.DataFrame, threshold: float = DEFAULT_ATTENDANCE_THRESHOLD
) -> bytes:
    """Generate a publication-grade PDF report and return the byte content."""
    if COL_ATTENDANCE_PCT not in df.columns:
        df = calculate_attendance_percentage(df)

    metrics = get_attendance_summary_metrics(df)
    dept_summary = get_department_summary(df)
    low_att_df = get_low_attendance_employees(df, threshold=threshold)
    insights = generate_workforce_insights(df, threshold=threshold)

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=4,
    )
    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=12,
    )
    heading2_style = ParagraphStyle(
        "DocH2",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=12,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "DocBody",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
    )
    body_bold = ParagraphStyle(
        "DocBodyBold",
        parent=body_style,
        fontName="Helvetica-Bold",
    )
    table_cell = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A202C"),
    )
    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=table_cell,
        fontName="Helvetica-Bold",
        textColor=colors.HexColor("#FFFFFF"),
    )

    story = []

    # Title & Header
    story.append(Paragraph(APP_TITLE, title_style))
    story.append(Paragraph(f"{APP_SUBTITLE} | Generated on {datetime.now().strftime('%B %d, %Y')}", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=12))

    # Executive Summary / KPI Cards Table
    story.append(Paragraph("1. Executive Attendance Summary", heading2_style))

    kpi_data = [
        [
            Paragraph("Total Workforce", table_cell),
            Paragraph(f"<b>{metrics['total_employees']}</b> employees", table_cell),
            Paragraph("Average Attendance", table_cell),
            Paragraph(f"<b>{metrics['average_attendance']:.2f}%</b>", table_cell),
        ],
        [
            Paragraph("Total Working Days", table_cell),
            Paragraph(f"{metrics['total_working_days']:,} days", table_cell),
            Paragraph("Total Present Days", table_cell),
            Paragraph(f"{metrics['total_present_days']:,} days", table_cell),
        ],
        [
            Paragraph("Total Absent Days", table_cell),
            Paragraph(f"{metrics['total_absent_days']:,} days", table_cell),
            Paragraph("Total Leave Days", table_cell),
            Paragraph(f"{metrics['total_leave_days']:,} days", table_cell),
        ],
        [
            Paragraph("Highest Attendance", table_cell),
            Paragraph(f"{metrics['highest_attendance']:.1f}% ({metrics['highest_employee_name']})", table_cell),
            Paragraph("Lowest Attendance", table_cell),
            Paragraph(f"{metrics['lowest_attendance']:.1f}% ({metrics['lowest_employee_name']})", table_cell),
        ],
    ]

    t_kpi = Table(kpi_data, colWidths=[120, 132, 120, 132])
    t_kpi.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
            ("PADDING", (0, 0), (-1, -1), 5),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )
    story.append(t_kpi)
    story.append(Spacer(1, 10))

    # Department Analysis Table
    story.append(Paragraph("2. Department-Wise Attendance Performance", heading2_style))

    dept_rows = [
        [
            Paragraph("Department", table_cell_bold),
            Paragraph("Employees", table_cell_bold),
            Paragraph("Avg Attendance", table_cell_bold),
            Paragraph("Present Days", table_cell_bold),
            Paragraph("Absent Days", table_cell_bold),
            Paragraph("Leave Days", table_cell_bold),
        ]
    ]

    for _, r in dept_summary.iterrows():
        dept_rows.append([
            Paragraph(str(r[COL_DEPT]), table_cell),
            Paragraph(str(int(r["Employee_Count"])), table_cell),
            Paragraph(f"{r['Average_Attendance_Pct']:.2f}%", table_cell),
            Paragraph(str(int(r["Total_Present_Days"])), table_cell),
            Paragraph(str(int(r["Total_Absent_Days"])), table_cell),
            Paragraph(str(int(r["Total_Leave_Days"])), table_cell),
        ])

    t_dept = Table(dept_rows, colWidths=[130, 64, 85, 75, 75, 75])
    t_dept.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2B6CB0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8F9FA")]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
            ("PADDING", (0, 0), (-1, -1), 4),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ])
    )
    story.append(t_dept)
    story.append(Spacer(1, 10))

    # Low Attendance Review Section
    story.append(Paragraph(f"3. Employees Requiring Attendance Review (< {threshold:.0f}%)", heading2_style))

    if low_att_df.empty:
        story.append(
            Paragraph(
                f"No employees are currently below the {threshold:.0f}% benchmark threshold.",
                body_style,
            )
        )
    else:
        low_rows = [
            [
                Paragraph("Emp ID", table_cell_bold),
                Paragraph("Name", table_cell_bold),
                Paragraph("Department", table_cell_bold),
                Paragraph("Present / Working", table_cell_bold),
                Paragraph("Attendance %", table_cell_bold),
            ]
        ]
        for _, lr in low_att_df.iterrows():
            low_rows.append([
                Paragraph(str(lr[COL_EMP_ID]), table_cell),
                Paragraph(str(lr[COL_NAME]), table_cell),
                Paragraph(str(lr[COL_DEPT]), table_cell),
                Paragraph(f"{int(lr[COL_PRESENT_DAYS])} / {int(lr[COL_WORKING_DAYS])}", table_cell),
                Paragraph(f"<b>{lr[COL_ATTENDANCE_PCT]:.2f}%</b>", table_cell),
            ])

        t_low = Table(low_rows, colWidths=[70, 144, 120, 90, 80])
        t_low.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C53030")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#FFF5F5")]),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#FEB2B2")),
                ("PADDING", (0, 0), (-1, -1), 4),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        story.append(t_low)

    story.append(Spacer(1, 10))

    # Workforce Insights & Analytical Observations
    story.append(Paragraph("4. Key Workforce Insights & Analytical Observations", heading2_style))

    for idx, ins in enumerate(insights, 1):
        color_hex = "#2B6CB0"
        if ins["type"] == "success":
            color_hex = "#2F855A"
        elif ins["type"] == "warning":
            color_hex = "#DD6B20"
        elif ins["type"] == "alert":
            color_hex = "#C53030"

        insight_header_style = ParagraphStyle(
            f"InsHeader_{idx}",
            parent=body_bold,
            textColor=colors.HexColor(color_hex),
        )

        p_title = Paragraph(f"• <b>[{ins['category'].upper()}]</b> {ins['title']}", insight_header_style)
        p_body = Paragraph(ins["message"], body_style)

        story.append(
            KeepTogether([
                p_title,
                Spacer(1, 2),
                p_body,
                Spacer(1, 6),
            ])
        )

    story.append(Spacer(1, 6))

    # Conclusion & Recommendations
    story.append(Paragraph("5. Concluding Recommendations", heading2_style))
    conclusion_text = (
        "Based on quantitative analysis of current attendance records, the organization demonstrates "
        "measurable workforce participation. To maintain operational continuity, it is recommended to "
        "conduct proactive counseling for individuals below benchmark attendance, ensure uniform policy "
        "enforcement across departments, and convert unplanned absences into pre-scheduled leaves."
    )
    story.append(Paragraph(conclusion_text, body_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    buffer.seek(0)
    return buffer.getvalue()
