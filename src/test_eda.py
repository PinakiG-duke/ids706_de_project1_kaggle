# src/test_eda.py
import pandas as pd
from pathlib import Path
from src import eda as eda_mod


def test_high_value_filter_p90():
    df = pd.DataFrame(
        {"Purchase_Amount_clean": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]}
    )
    top, thr = eda_mod.high_value_filter(df, "Purchase_Amount_clean", q=0.90)
    assert thr == 90
    assert set(top["Purchase_Amount_clean"]) == {90, 100}


def test_summarize_by_category_schema():
    df = pd.DataFrame(
        {
            "Customer_ID": [1, 2, 3, 4],
            "Purchase_Category": ["A", "A", "B", "B"],
            "Purchase_Amount_clean": [10, 20, 30, 40],
            "Customer_Satisfaction": [3, 4, 5, 6],
            "Discount_Used": [0, 1, 1, 0],
        }
    )
    out = eda_mod.summarize_by_category(df)
    assert {"n", "avg_amount", "avg_satisfaction", "discount_rate"}.issubset(
        out.columns
    )


def test_run_eda_writes_artifacts(tmp_path, monkeypatch):
    # Redirect artifacts to a temp folder
    monkeypatch.setattr(eda_mod, "ART", tmp_path / "artifacts")

    # Makes a CSV; run EDA end-to-end
    csv = tmp_path / "mini.csv"
    pd.DataFrame(
        {
            "Customer_ID": [1, 2, 3],
            "Purchase_Amount": ["$10", "$20", "$30"],
            "Time_of_Purchase": ["01/01/2024", "01-02-2024", "bad"],
            "Purchase_Category": ["A", "B", "A"],
            "Customer_Satisfaction": [3, 4, 5],
            "Discount_Used": [0, 1, 0],
        }
    ).to_csv(csv, index=False)

    # run_eda should accept a path
    eda_mod.run_eda(str(csv))

    must_exist = [
        "eda_head.csv",
        "eda_info.txt",
        "eda_describe.csv",
        "eda_missing.csv",
        "eda_duplicates.txt",
        "eda_filter_stats.csv",
        "eda_category_summary.csv",
    ]
    for name in must_exist:
        assert (eda_mod.ART / name).exists()
