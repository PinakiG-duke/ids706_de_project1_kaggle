"""
Data Cleaning Module
- Load a local CSV
- Clean currency strings in Purchase_Amount to float (Purchase_Amount_clean)
- Parse Time_of_Purchase when it contains a DATE (MM/DD/YYYY or MM-DD-YYYY)
   - Create: Purchase_Date (datetime64)
   - Create: Purchase_Year, Purchase_Month, Purchase_Day, Purchase_DayOfWeek
- Save a processed copy to data/processed/
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd

# After (pure refactoring)
from pathlib import Path

DEFAULT_CSV = Path("data/raw/Ecommerce_Consumer_Behavior_Analysis_Data.csv")


def clean_purchase_amount(s: pd.Series) -> pd.Series:
    """
    Normalize currency-like values to float.
    Handles: '$', ',', surrounding spaces, empty strings, 'None'/'NaN' strings, (negatives).
    Returns float dtype with NaN where parsing fails.
    """
    if s is None:
        return pd.Series(dtype="float64")

    # Coerce everything to string for safe text ops
    t = s.astype(str).str.strip()

    # Map common "missing" string tokens to NA
    t = t.replace({"": pd.NA, "None": pd.NA, "none": pd.NA, "NaN": pd.NA, "nan": pd.NA})

    # Remove currency formatting
    t = t.str.replace(r"[\$,]", "", regex=True)

    # Convert (123.45) to -123.45 if you ever see accounting negatives
    t = t.str.replace(r"^\((.*)\)$", r"-\1", regex=True)

    # Final numeric coercion (anything invalid -> NaN)
    return pd.to_numeric(t, errors="coerce")


def parse_purchase_date(series: pd.Series) -> pd.Series:
    """
    Parse dates identified to be mixed as 'MM/DD/YYYY' or 'MM-DD-YYYY'.
    Strategy:
      - Normalize separators to '/'
      - Strictly parse with format='%m/%d/%Y' to avoid ambiguous day-first issues
    Returns pandas datetime64[ns]; invalid rows become NaN.
    """
    # Normalize separators and whitespace
    s = (
        series.astype(str)
        .str.strip()
        .str.replace(r"[-\.]", "/", regex=True)  # '-', '.' -> '/'
    )

    # Try strict month/day/year with 4-digit year
    dt = pd.to_datetime(s, format="%m/%d/%Y", errors="coerce")

    return dt


# Refactoring - Rename dt to date_series


def add_date_features(
    df: pd.DataFrame, date_col: str = "Purchase_Date"
) -> pd.DataFrame:
    """
    Given a datetime64 column, add date-related features.
    Creates: Purchase_Year, Purchase_Month, Purchase_Day, Purchase_DayOfWeek (name).
    """
    if date_col in df.columns:
        date_series = df[date_col]
        df["Purchase_Year"] = date_series.dt.year
        df["Purchase_Month"] = date_series.dt.month
        df["Purchase_Day"] = date_series.dt.day
        df["Purchase_DayOfWeek"] = date_series.dt.day_name()
    return df


# Extracted helper for saving processed CSV
def _save_processed(df: pd.DataFrame, out_dir: Path = Path("data/processed")) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_dir / "ecom_clean.csv", index=False)


# --------- main cleaning module ---------


def load_and_clean(
    csv_path: str | Path | None = None, save_processed: bool = False
) -> pd.DataFrame:
    """
    Load CSV and add cleaned columns; optionally save processed CSV.
    If csv_path is None, use DEFAULT_CSV.
    """
    p = Path(csv_path) if csv_path is not None else DEFAULT_CSV
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {p.resolve()}")

    # Refactoring - Extract variable

    raw_df = pd.read_csv(p)
    df = raw_df.copy()

    # 1)Clean Purchase_Amount to float
    if "Purchase_Amount" in df.columns:
        df["Purchase_Amount_clean"] = clean_purchase_amount(df["Purchase_Amount"])

    # 2)Parse Purchase_Date from Time_of_Purchase if it contains a date

    if "Time_of_Purchase" in df.columns:
        df["Purchase_Date"] = parse_purchase_date(df["Time_of_Purchase"])
        df = add_date_features(df, "Purchase_Date")

    # 3) Save processed CSV- Also gives a checkpoint for manual inspection
    # Refactored - Extracted helper for saving processed csv

    if save_processed:
        _save_processed(df)
        # out_dir = Path("data/processed"); out_dir.mkdir(parents=True, exist_ok=True)
        # df.to_csv(out_dir / "ecom_clean.csv", index=False)

    return df


# Allow running this file directly for a quick check
if __name__ == "__main__":
    _df = load_and_clean(DEFAULT_CSV, save_processed=True)
    print(_df.head())
