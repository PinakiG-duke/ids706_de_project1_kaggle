"""
Exploratory Data Analysis (EDA) module
- Saves head (first rows) -> artifacts/eda_head.csv
- Saves numeric/bool describe -> artifacts/eda_describe.csv
- Saves missing counts -> artifacts/eda_missing.csv
- Saves duplicate count -> artifacts/eda_duplicates.txt
- Saves filter stats (median + rows kept) -> artifacts/eda_filter_stats.csv
- Saves category summary (groupby) -> artifacts/eda_category_summary.csv
"""

from __future__ import annotations
from pathlib import Path
import numpy as np
import pandas as pd
import io

from .data_clean import load_and_clean, DEFAULT_CSV

ART = Path("artifacts")
ART.mkdir(parents=True, exist_ok=True)

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def high_value_filter(df: pd.DataFrame, col: str, q: float = 0.10):
    """Keep rows where col >= q-quantile ( q=0.10 keeps top 90%).
    This is a placeholder function which can be used to remove outliers from the data """
    threshold = float(df[col].quantile(q, interpolation="nearest"))
    return df[df[col] >= threshold], threshold


def summarize_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Group by Purchase_Category with named aggregation.
    Creates summary stats:
      - n: count of orders
      - avg_amount: mean Purchase_Amount_clean
      - avg_satisfaction: mean Customer_Satisfaction
      - share_of_trans_on_disc: mean Discount_Used
    This is a placeholder function which can be used to create summaries across other attributes for eg: Customer gender, marital status, brand loyalty
    """
    named_aggs: dict[str, tuple[str, str]] = {"n": ("Customer_ID", "count")}
    if "Purchase_Amount_clean" in df.columns:
        named_aggs["avg_amount"] = ("Purchase_Amount_clean", "mean")
    if "Customer_Satisfaction" in df.columns:
        named_aggs["avg_satisfaction"] = ("Customer_Satisfaction", "mean")
    if "Discount_Used" in df.columns:
        named_aggs["share_of_trans_on_disc"] = ("Discount_Used", "mean")

    out = (
        df.groupby("Purchase_Category", dropna=False)
          .agg(n=("Customer_ID", "size"),
        avg_amount=("Purchase_Amount_clean", "mean"),
        avg_satisfaction=("Customer_Satisfaction", "mean"),
        discount_rate=("Discount_Used", "mean"),)
          .reset_index()
    )
    return out


def run_eda(csv_path: str | Path = None):
    ensure_dir(ART)
    if csv_path is None:
        csv_path = DEFAULT_CSV
    df = load_and_clean(csv_path)

    # 1) Head (preview rows)
    df.head().to_csv(ART / "eda_head.csv", index=False)

    # 2) Info -> write as plain text file
    sio = io.StringIO()
    df.info(buf=sio)
    (ART / "eda_info.txt").write_text(sio.getvalue(), encoding="utf-8")

    # 3) Describe numeric/bool
    desc = df.select_dtypes(include=[np.number, "bool"]).describe().round(2)
    if not desc.empty:
        desc.to_csv(ART / "eda_describe.csv")

    # 4) Missing values per column
    df.isna().sum().rename("n_missing").to_frame().to_csv(ART / "eda_missing.csv")

    # 5) Duplicate rows (count)
    dupes = int(df.duplicated().sum())
    (ART / "eda_duplicates.txt").write_text(str(dupes), encoding="utf-8")

    # 6) Filter: high-value orders (if amount exists)
    if "Purchase_Amount_clean" in df.columns:
        high, thr = high_value_filter(df, "Purchase_Amount_clean", q=0.10)
        pd.DataFrame(
        {
            "percentile": ["p90"],
            "threshold_value": [round(thr, 2)],
            "rows_kept": [len(high)],
            "rows_total": [len(df)],
            "kept_share": [round(len(high) / len(df), 4)]
        }
        ).to_csv(ART / "eda_filter_stats.csv", index=False)

    # 7) Groupby summary by category (Purchase_Category)
    if "Purchase_Category" in df.columns:
        summarize_by_category(df).to_csv(ART / "eda_category_summary.csv")

    print("EDA CSV files written to ./artifacts")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default=None, help="Path to input CSV")
    args = ap.parse_args()
    run_eda()
