# src/test_model.py
import pandas as pd
from src.model import train_on_df

def test_train_on_df_ok_numeric_only():
    df = pd.DataFrame({
        "Purchase_Amount_clean":[100,250,300,150,400,220,180,330],
        "Customer_Satisfaction":[5,6,7,4,8,6,5,7],
        "Return_Rate":[0.05,0.1,0.0,0.15,0.02,0.08,0.12,0.03],
        "Discount_Used":[0,1,1,0,1,1,0,1],
    })
    res = train_on_df(df, write_artifacts=False)
    assert res["ok"] is True
    assert 0.0 <= res["accuracy"] <= 1.0
    assert res["n_features"] >= 1

def test_train_on_df_missing_target():
    df = pd.DataFrame({"x":[1,2,3], "y":[0.1,0.2,0.3]})
    res = train_on_df(df, write_artifacts=False)
    assert res["ok"] is False and res["reason"] == "missing target"
