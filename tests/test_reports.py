"""Tests for PDF, Excel, and CSV report generators."""

import pandas as pd
from app.reports.pdf_report import generate_pdf_report
from app.reports.excel_report import generate_excel_report
from app.data.loader import load_attendance_data
from app.config import DEFAULT_DATA_PATH


def test_pdf_report_generation():
    """Verify PDF report creates non-empty binary output with valid PDF header."""
    df, _ = load_attendance_data(DEFAULT_DATA_PATH)
    assert df is not None

    pdf_bytes = generate_pdf_report(df, threshold=80.0)
    assert isinstance(pdf_bytes, bytes)
    assert len(pdf_bytes) > 1000
    # PDF files start with %PDF
    assert pdf_bytes.startswith(b"%PDF")


def test_excel_report_generation():
    """Verify Excel report creates valid non-empty openpyxl binary file."""
    df, _ = load_attendance_data(DEFAULT_DATA_PATH)
    assert df is not None

    excel_bytes = generate_excel_report(df, threshold=80.0)
    assert isinstance(excel_bytes, bytes)
    assert len(excel_bytes) > 1000
    # Modern xlsx files are zip archives starting with PK
    assert excel_bytes.startswith(b"PK")
