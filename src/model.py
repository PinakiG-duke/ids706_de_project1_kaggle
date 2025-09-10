"""
Simple Logistic Regression Model which takes only numeric or bool attributes to predict discount (Y/N)

- Loads the cleaned dataframe (uses src.data_clean.load_and_clean)
- Uses ONLY numeric/bool columns
- Trains a LogisticRegression to predict Discount_Used
- Writes a short txt report to artifacts/model_report.txt
"""

from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from .data_clean import load_and_clean, DEFAULT_CSV

ART = Path("artifacts")
ART.mkdir(parents=True, exist_ok=True)


def train_on_df(df: pd.DataFrame, write_artifacts: bool = True) -> dict:
    """
    Train a logistic regression using only numeric/bool features.
    Returns {'ok': bool, 'accuracy': float, 'n_features': int, ...}.
    """
    if "Discount_Used" not in df.columns:
        if write_artifacts:
            (ART / "model_report.txt").write_text(
                "No 'Discount_Used' column; skipping model.", encoding="utf-8"
            )
        return {"ok": False, "reason": "missing target"}

    # Target
    y = df["Discount_Used"].astype(int)

    # Drop some features (This is a placeholder that can be used to drop features we dont want to include in the model)
    drop = {"Discount_Used", "Customer_ID", "Purchase_Amount", "Time_of_Purchase"}
    X = df.drop(columns=[c for c in drop if c in df.columns])

    # Only numeric/bool attributes are retained - Placeholder for inclusion of attributes to the model
    num_cols = X.select_dtypes(include=["number", "bool"]).columns.tolist()
    if not num_cols:
        if write_artifacts:
            (ART / "model_report.txt").write_text(
                "No numeric/bool features available; skipping model.", encoding="utf-8"
            )
        return {"ok": False, "reason": "no numeric features"}

    X = X[num_cols].copy()
    X = X.fillna(X.median(numeric_only=True))  # simple imputation

    # Split dataset into test and train the model
    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )
    clf = LogisticRegression(max_iter=1000)
    clf.fit(Xtr, ytr)

    acc = accuracy_score(yte, clf.predict(Xte))
    result = {"ok": True, "accuracy": float(acc), "n_features": len(num_cols)}

    if write_artifacts:
        report = (
            "Baseline model: Logistic Regression (numeric-only)\n"
            f"Rows: {len(df)}  |  Features used: {len(num_cols)}\n"
            "Target: Discount_Used (binary)\n"
            "Train/Test: 90/10 (stratified)\n"
            f"Accuracy: {acc:.3f}\n"
            f"Feature columns: {', '.join(num_cols)}\n"
        )
        (ART / "model_report.txt").write_text(report, encoding="utf-8")

    return result


def run_baseline(csv_path: str = DEFAULT_CSV) -> dict:
    """Load cleaned CSV and train the model."""
    df = load_and_clean(csv_path)
    return train_on_df(df, write_artifacts=True)


if __name__ == "__main__":
    res = run_baseline()
    if res.get("ok"):
        print(f"Model OK — accuracy: {res['accuracy']:.3f}, features: {res['n_features']}")
    else:
        print("Model skipped:", res.get("reason"))
