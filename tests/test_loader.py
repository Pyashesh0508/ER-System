"""Tests for CSV data loading module."""

from pathlib import Path
import pandas as pd
from app.data.loader import load_attendance_data
from app.config import DEFAULT_DATA_PATH, SAMPLE_DATA_PATH


def test_load_default_attendance_data():
    """Verify loading the default attendance CSV."""
    df, err = load_attendance_data(DEFAULT_DATA_PATH)
    assert err is None
    assert df is not None
    assert not df.empty
    assert len(df) >= 20
    assert "Employee_ID" in df.columns
    assert "Name" in df.columns


def test_load_sample_attendance_data():
    """Verify loading the sample attendance CSV."""
    df, err = load_attendance_data(SAMPLE_DATA_PATH)
    assert err is None
    assert df is not None
    assert not df.empty
    assert len(df) == 10


def test_load_non_existent_file():
    """Verify proper error response for missing file."""
    fake_path = Path("data/non_existent_file_xyz.csv")
    df, err = load_attendance_data(fake_path)
    assert df is None
    assert err is not None
    assert "File not found" in err
