"""
DATA CLEANING
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

DEFAULT_CSV = "data/raw/Ecommerce_Consumer_Behavior_Analysis_Data.csv"

def clean_purchase_amount(series: pd.Series) -> pd.Series:
    """Turn '$1,234.50' to 1234.50 (float)"""
    return (
        series.astype(str)
              .str.replace(r"[\$,]", "", regex=True)
              .replace({"": np.nan})
              .astype(float)
    )

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


def add_date_features(df: pd.DataFrame, date_col: str = "Purchase_Date") -> pd.DataFrame:
    """
    Given a datetime64 column, add date-related features.
    Creates: Purchase_Year, Purchase_Month, Purchase_Day, Purchase_DayOfWeek (name).
    """
    if date_col in df.columns:
        dt = df[date_col]
        df["Purchase_Year"] = dt.dt.year
        df["Purchase_Month"] = dt.dt.month
        df["Purchase_Day"] = dt.dt.day
        df["Purchase_DayOfWeek"] = dt.dt.day_name()
    return df

# --------- main cleaning entrypoint ---------

def load_and_clean(csv_path: str | Path = DEFAULT_CSV, save_processed: bool = False) -> pd.DataFrame:
    """Load CSV and add cleaned columns; saves processed CSV """
    p = Path(csv_path)
    if not p.exists():
        raise FileNotFoundError(f"CSV not found: {p.resolve()}")
    df = pd.read_csv(p)

    # 1)Clean Purchase_Amount to float
    if "Purchase_Amount" in df.columns:
        df["Purchase_Amount_clean"] = clean_purchase_amount(df["Purchase_Amount"])

    # 2)Parse Purchase_Date from Time_of_Purchase if it contains a date

    if "Time_of_Purchase" in df.columns:
        df["Purchase_Date"] = parse_purchase_date(df["Time_of_Purchase"])
        df = add_date_features(df, "Purchase_Date")

    # 3) Save processed CSV- Also gives a checkpoint for manual inspection

    if save_processed:
        out_dir = Path("data/processed"); out_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_dir / "ecom_clean.csv", index=False)

    return df

# Allow running this file directly for a quick check
if __name__ == "__main__":
    _df = load_and_clean(DEFAULT_CSV, save_processed=True)
    print(_df.head())
