"""File reading and parsing helpers for .csv, .xlsx, and .xls spreadsheets."""
from pathlib import Path
from typing import List, Dict, Any, Tuple
import pandas as pd
from app.utils.logger import logger

def inspect_file_columns(file_path: str) -> List[str]:
    """Reads the header row of a file and returns the list of column names."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()
    if ext == ".csv":
        df = pd.read_csv(file_path, nrows=0, dtype=str)
    elif ext == ".xlsx":
        df = pd.read_excel(file_path, nrows=0, dtype=str, engine="openpyxl")
    elif ext == ".xls":
        df = pd.read_excel(file_path, nrows=0, dtype=str, engine="xlrd")
    else:
        raise ValueError(f"Unsupported file format: {ext}. Only .csv, .xlsx, and .xls are supported.")

    return [str(col).strip() for col in df.columns]

def read_spreadsheet(file_path: str) -> pd.DataFrame:
    """
    Reads an entire spreadsheet (.csv, .xlsx, or .xls) into a pandas DataFrame.
    All data is initially read as strings to preserve leading zeros in phone numbers.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()
    logger.info(f"Reading spreadsheet: {file_path} (format: {ext})")

    if ext == ".csv":
        # Handle potential encoding issues (utf-8, latin-1)
        try:
            df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
        except UnicodeDecodeError:
            df = pd.read_csv(file_path, dtype=str, keep_default_na=False, encoding="latin-1")
    elif ext == ".xlsx":
        df = pd.read_excel(file_path, dtype=str, keep_default_na=False, engine="openpyxl")
    elif ext == ".xls":
        df = pd.read_excel(file_path, dtype=str, keep_default_na=False, engine="xlrd")
    else:
        raise ValueError(f"Unsupported spreadsheet format: {ext}")

    # Strip whitespace from column headers
    df.columns = [str(col).strip() for col in df.columns]
    return df
