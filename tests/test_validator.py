"""Tests for dataset validation and sanitization."""

import pandas as pd
from app.data.validator import validate_attendance_dataframe


def test_validator_valid_dataset():
    """Verify validation passes for valid dataset."""
    valid_data = pd.DataFrame({
        "Employee_ID": ["E01", "E02"],
        "Name": ["Alice", "Bob"],
        "Department": ["Tech", "HR"],
        "Working_Days": [25, 25],
        "Present_Days": [20, 25],
        "Absent_Days": [3, 0],
        "Leave_Days": [2, 0],
    })
    res = validate_attendance_dataframe(valid_data)
    assert res.is_valid is True
    assert len(res.errors) == 0
    assert res.cleaned_df is not None


def test_validator_missing_column():
    """Verify validation fails when a required column is missing."""
    invalid_data = pd.DataFrame({
        "Employee_ID": ["E01"],
        "Name": ["Alice"],
        # Department is missing
        "Working_Days": [25],
        "Present_Days": [20],
        "Absent_Days": [3],
        "Leave_Days": [2],
    })
    res = validate_attendance_dataframe(invalid_data)
    assert res.is_valid is False
    assert any("Missing required column" in err for err in res.errors)


def test_validator_negative_days():
    """Verify validation catches negative days."""
    invalid_data = pd.DataFrame({
        "Employee_ID": ["E01"],
        "Name": ["Alice"],
        "Department": ["Tech"],
        "Working_Days": [25],
        "Present_Days": [-5],
        "Absent_Days": [3],
        "Leave_Days": [2],
    })
    res = validate_attendance_dataframe(invalid_data)
    assert res.is_valid is False
    assert any("negative values" in err for err in res.errors)


def test_validator_zero_working_days():
    """Verify validation catches zero working days."""
    invalid_data = pd.DataFrame({
        "Employee_ID": ["E01"],
        "Name": ["Alice"],
        "Department": ["Tech"],
        "Working_Days": [0],
        "Present_Days": [0],
        "Absent_Days": [0],
        "Leave_Days": [0],
    })
    res = validate_attendance_dataframe(invalid_data)
    assert res.is_valid is False
    assert any("greater than zero" in err for err in res.errors)


def test_validator_present_exceeds_working():
    """Verify validation catches present days greater than working days."""
    invalid_data = pd.DataFrame({
        "Employee_ID": ["E01"],
        "Name": ["Alice"],
        "Department": ["Tech"],
        "Working_Days": [20],
        "Present_Days": [22],
        "Absent_Days": [0],
        "Leave_Days": [0],
    })
    res = validate_attendance_dataframe(invalid_data)
    assert res.is_valid is False
    assert any("exceeds Working_Days" in err for err in res.errors)
