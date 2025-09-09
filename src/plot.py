"""
PLOT
- Histogram of Purchase_Amount_clean
- Saves the plot as a png file into the artifacts folder
"""

from __future__ import annotations
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

from .data_clean import load_and_clean, DEFAULT_CSV

ART = Path("artifacts"); ART.mkdir(parents=True, exist_ok=True)

def make_histogram(csv_path: str = DEFAULT_CSV):
    df = load_and_clean(csv_path)

    # Plot the cleaned amount; otherwise first numeric column
    col = "Purchase_Amount_clean" if "Purchase_Amount_clean" in df.columns else None
    if col is None:
        nums = df.select_dtypes(include=["number", "bool"]).columns.tolist()
        if not nums:
            print("No numeric columns available for plotting.")
            return
        col = nums[0]

    plt.figure()
    df[col].hist(bins=20)
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Count of transactions")
    plt.tight_layout()
    out = ART / "hist_purchase_amount_plot.png"
    plt.savefig(out, dpi=150)
    print(f"Wrote {out}")

if __name__ == "__main__":
    make_histogram()
