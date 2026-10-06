"""Data loader module for reading CSV datasets."""

from io import StringIO, BytesIO
from pathlib import Path
from typing import Union, Tuple, Optional
import pandas as pd

from app.config import DEFAULT_DATA_PATH


def _read_with_encodings(source: Union[str, Path, BytesIO]) -> pd.DataFrame:
    """Attempt reading CSV data using common encodings."""
    encodings = ["utf-8", "utf-8-sig", "latin1", "cp1252"]
    last_err: Optional[Exception] = None

    for enc in encodings:
        try:
            if isinstance(source, (str, Path)):
                return pd.read_csv(source, encoding=enc)
            elif isinstance(source, BytesIO):
                source.seek(0)
                return pd.read_csv(source, encoding=enc)
            else:
                return pd.read_csv(source, encoding=enc)
        except UnicodeDecodeError as e:
            last_err = e
            continue
        except pd.errors.ParserError as e:
            raise ValueError(f"Malformed CSV format detected: {str(e)}") from e

    if last_err:
        raise ValueError(f"Failed to decode CSV file with standard encodings: {str(last_err)}")
    raise ValueError("Unable to read CSV file.")


def load_attendance_data(file_path: Union[str, Path] = DEFAULT_DATA_PATH) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Load employee attendance dataset from a local file path.

    Returns:
        (df, error_message): Tuple containing DataFrame if successful, or error message.
    """
    path = Path(file_path)
    if not path.exists():
        return None, f"File not found: '{path.as_posix()}'. Please ensure the dataset exists."

    if not path.is_file():
        return None, f"The path '{path.as_posix()}' is not a valid file."

    try:
        df = _read_with_encodings(path)
        if df.empty:
            return None, "The CSV file is empty."
        return df, None
    except Exception as e:
        return None, f"Error loading CSV file '{path.name}': {str(e)}"


def load_csv_from_upload(uploaded_file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Load employee attendance data from a Streamlit UploadedFile object.

    Returns:
        (df, error_message): Tuple containing DataFrame if successful, or error message.
    """
    if uploaded_file is None:
        return None, "No file uploaded."

    try:
        # Check bytes or file-like object
        bytes_data = uploaded_file.getvalue()
        if not bytes_data or len(bytes_data.strip()) == 0:
            return None, "The uploaded file is empty."

        bio = BytesIO(bytes_data)
        df = _read_with_encodings(bio)
        if df.empty:
            return None, "The uploaded file contains no data rows."
        return df, None
    except Exception as e:
        return None, f"Error processing uploaded file '{uploaded_file.name}': {str(e)}"
