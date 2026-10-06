"""Data validation module for employee attendance datasets."""

from dataclasses import dataclass, field
from typing import List, Optional
import pandas as pd

from app.config import (
    COL_EMP_ID,
    COL_NAME,
    COL_DEPT,
    COL_WORKING_DAYS,
    COL_PRESENT_DAYS,
    COL_ABSENT_DAYS,
    COL_LEAVE_DAYS,
    REQUIRED_COLUMNS,
    NUMERIC_COLUMNS,
)


@dataclass
class ValidationResult:
    """Represents the outcome of dataset validation."""

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    cleaned_df: Optional[pd.DataFrame] = None

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0


def validate_attendance_dataframe(df: pd.DataFrame) -> ValidationResult:
    """Validate and clean an employee attendance DataFrame.

    Checks:
    - Non-empty DataFrame
    - Presence of required columns
    - Valid non-empty employee names
    - Non-duplicate employee IDs
    - Numeric validity for days columns
    - Non-negative values for Present, Absent, and Leave days
    - Working_Days > 0
    - Present_Days <= Working_Days
    - Present + Absent + Leave logical consistency warnings

    Returns:
        ValidationResult containing validation status, error/warning messages, and cleaned DataFrame.
    """
    errors: List[str] = []
    warnings: List[str] = []

    if df is None or df.empty:
        return ValidationResult(
            is_valid=False,
            errors=["The provided dataset is empty. Please provide a valid CSV file."],
        )

    # Clean column names (strip whitespace)
    working_df = df.copy()
    working_df.columns = [str(c).strip() for c in working_df.columns]

    # Check required columns
    missing_cols = [c for c in REQUIRED_COLUMNS if c not in working_df.columns]
    if missing_cols:
        errors.append(
            f"Missing required column(s): {', '.join(missing_cols)}. "
            f"Expected columns are: {', '.join(REQUIRED_COLUMNS)}."
        )
        return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

    # Check for empty employee names
    working_df[COL_NAME] = working_df[COL_NAME].astype(str).str.strip()
    empty_names_mask = (working_df[COL_NAME] == "") | (working_df[COL_NAME].str.lower() == "nan")
    if empty_names_mask.any():
        bad_indices = working_df.index[empty_names_mask].tolist()
        errors.append(
            f"Employee names cannot be empty. Found empty name at row index: {bad_indices}."
        )

    # Check employee IDs
    working_df[COL_EMP_ID] = working_df[COL_EMP_ID].astype(str).str.strip()
    empty_ids_mask = (working_df[COL_EMP_ID] == "") | (working_df[COL_EMP_ID].str.lower() == "nan")
    if empty_ids_mask.any():
        bad_indices = working_df.index[empty_ids_mask].tolist()
        errors.append(
            f"Employee IDs cannot be empty. Found empty ID at row index: {bad_indices}."
        )

    # Check duplicate Employee IDs
    duplicate_ids = working_df[COL_EMP_ID][working_df[COL_EMP_ID].duplicated()].tolist()
    if duplicate_ids:
        warnings.append(
            f"Duplicate Employee IDs detected: {', '.join(map(str, set(duplicate_ids)))}. "
            f"Ensure each employee has a unique identifier."
        )

    # Check department
    working_df[COL_DEPT] = working_df[COL_DEPT].astype(str).str.strip()
    empty_dept_mask = (working_df[COL_DEPT] == "") | (working_df[COL_DEPT].str.lower() == "nan")
    if empty_dept_mask.any():
        warnings.append("Some records have missing or blank department names. They have been preserved.")

    # Validate numeric columns
    for num_col in NUMERIC_COLUMNS:
        converted = pd.to_numeric(working_df[num_col], errors="coerce")
        nan_mask = converted.isna()
        if nan_mask.any():
            bad_indices = working_df.index[nan_mask].tolist()
            errors.append(
                f"Column '{num_col}' contains invalid or non-numeric values at row index: {bad_indices}."
            )
        else:
            working_df[num_col] = converted

    # If numeric conversion failed, stop before relational checks
    if errors:
        return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

    # Relational and range checks
    # Working days must be > 0
    zero_working = working_df[working_df[COL_WORKING_DAYS] <= 0]
    if not zero_working.empty:
        bad_ids = zero_working[COL_EMP_ID].tolist()
        errors.append(
            f"Working_Days must be greater than zero. Invalid records for employees: {bad_ids}."
        )

    # Non-negative checks
    for col in [COL_PRESENT_DAYS, COL_ABSENT_DAYS, COL_LEAVE_DAYS]:
        negative_records = working_df[working_df[col] < 0]
        if not negative_records.empty:
            bad_ids = negative_records[COL_EMP_ID].tolist()
            errors.append(
                f"Column '{col}' cannot contain negative values. Invalid records for employees: {bad_ids}."
            )

    # Present days should not exceed working days
    excess_present = working_df[working_df[COL_PRESENT_DAYS] > working_df[COL_WORKING_DAYS]]
    if not excess_present.empty:
        bad_ids = excess_present[COL_EMP_ID].tolist()
        errors.append(
            f"Present_Days exceeds Working_Days for employees: {bad_ids}."
        )

    # Check Present + Absent + Leave vs Working Days
    total_accounted = (
        working_df[COL_PRESENT_DAYS]
        + working_df[COL_ABSENT_DAYS]
        + working_df[COL_LEAVE_DAYS]
    )
    mismatched = working_df[total_accounted > working_df[COL_WORKING_DAYS]]
    if not mismatched.empty:
        bad_ids = mismatched[COL_EMP_ID].tolist()
        warnings.append(
            f"Sum of (Present + Absent + Leave) days exceeds Working_Days for employees: {bad_ids}. "
            "Please verify attendance records."
        )

    if errors:
        return ValidationResult(is_valid=False, errors=errors, warnings=warnings)

    return ValidationResult(
        is_valid=True,
        errors=[],
        warnings=warnings,
        cleaned_df=working_df,
    )
