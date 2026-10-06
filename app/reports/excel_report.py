"""Excel report generator using openpyxl."""

from io import BytesIO
from typing import List, Dict
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from app.analysis.attendance import calculate_attendance_percentage
from app.analysis.department import get_department_summary
from app.analysis.insights import generate_workforce_insights


def generate_excel_report(
    df: pd.DataFrame, threshold: float = 80.0
) -> bytes:
    """Generate a multi-sheet Excel workbook as bytes.

    Sheets:
    1. Employee Data
    2. Department Summary
    3. Workforce Insights
    """
    if COL_ATTENDANCE_PCT := "Attendance_Percentage":
        if COL_ATTENDANCE_PCT not in df.columns:
            df = calculate_attendance_percentage(df)

    dept_summary = get_department_summary(df)
    insights_list = generate_workforce_insights(df, threshold=threshold)
    insights_df = pd.DataFrame(insights_list)

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        # Write sheets
        df.to_excel(writer, sheet_name="Employee Data", index=False)
        dept_summary.to_excel(writer, sheet_name="Department Summary", index=False)
        if not insights_df.empty:
            insights_df.rename(
                columns={
                    "category": "Category",
                    "type": "Severity",
                    "title": "Finding Title",
                    "message": "Analytical Observation",
                }
            ).to_excel(writer, sheet_name="Workforce Insights", index=False)

        # Style each sheet
        header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        thin_border = Border(
            left=Side(style="thin", color="D3D3D3"),
            right=Side(style="thin", color="D3D3D3"),
            top=Side(style="thin", color="D3D3D3"),
            bottom=Side(style="thin", color="D3D3D3"),
        )

        for sheetname in writer.sheets:
            ws = writer.sheets[sheetname]
            ws.views.sheetView[0].showGridLines = True

            # Style header row
            for col_idx in range(1, ws.max_column + 1):
                cell = ws.cell(row=1, column=col_idx)
                cell.fill = header_fill
                cell.font = header_font
                cell.alignment = Alignment(horizontal="center", vertical="center")

            # Style data rows and auto-fit column widths
            for col_idx in range(1, ws.max_column + 1):
                col_letter = get_column_letter(col_idx)
                max_len = 0
                for row_idx in range(1, ws.max_row + 1):
                    cell = ws.cell(row=row_idx, column=col_idx)
                    cell.border = thin_border
                    if row_idx > 1:
                        cell.font = Font(name="Calibri", size=10)
                        # Center align short fields or numbers
                        if isinstance(cell.value, (int, float)):
                            cell.alignment = Alignment(horizontal="right", vertical="center")
                        else:
                            cell.alignment = Alignment(horizontal="left", vertical="center")
                    val_str = str(cell.value or "")
                    if len(val_str) > max_len:
                        max_len = len(val_str)

                ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    output.seek(0)
    return output.getvalue()
