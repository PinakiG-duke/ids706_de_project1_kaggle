"""

    Unit tests for the simple, numeric-only baseline model in `src.model`.
    These tests exercise the public function `train_on_df`, which trains a
    LogisticRegression on numeric/bool columns only and returns a small result dict.

    This is also a stakeholder to keep on adding test cases including edge cases

    1) Expected result for the tiny synthetic numeric dataset:
       - returns ok=True
       - accuracy is a float in [0, 1]
       - at least one feature was used
    2) Exception handling when the target column 'Discount_Used' is missing:
       - returns ok=False with reason 'missing target'

Some key limitations of the current test case (will be expanded subsequently):

    - No file I/O: tests call `train_on_df(..., write_artifacts=False)` so nothing is written.
    - No external data: tests build DataFrames inline.
    - Deterministic split in the model (random_state=42) keeps results stable.

What this test case does
    - Verifies the model entrypoint behaves correctly.
    - Demonstrates basic test coverage
"""

import pandas as pd
from src.model import train_on_df


def test_train_on_df_ok():
    # Small Syntetic data to be tested-Placeholder to add more test cases to evaluate
    df = pd.DataFrame(
        {
            "Purchase_Amount_clean": [100, 250, 300, 150, 400, 220, 180, 330],
            "Product_Rating": [3.2, 4.1, 4.8, 2.9, 4.0, 3.7, 3.1, 4.4],
            "Return_Rate": [0.05, 0.10, 0.00, 0.15, 0.02, 0.08, 0.12, 0.03],
            "Customer_Satisfaction": [5, 6, 7, 4, 8, 6, 5, 7],
            "Discount_Used": [0, 1, 1, 0, 1, 1, 0, 1],  # target
        }
    )
    res = train_on_df(df, write_artifacts=False)
    assert res["ok"] is True
    assert 0.0 <= res["accuracy"] <= 1.0
    assert res["n_features"] >= 1


def test_train_on_df_missing_target():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [0.1, 0.2, 0.3]})
    res = train_on_df(df, write_artifacts=False)
    assert res["ok"] is False
    assert res["reason"] == "missing target"
