# test_clean.py
import pandas as pd
from src.data_clean import clean_purchase_amount, parse_purchase_date, load_and_clean

def test_clean_purchase_amount_basic():
    s = pd.Series(["$1,234.50", "  89.00", "", None, "None"])
    out = clean_purchase_amount(s)
    assert out.iloc[0] == 1234.50
    assert out.iloc[1] == 89.00
    assert pd.isna(out.iloc[2]) and pd.isna(out.iloc[3])

def test_parse_purchase_date_mixed_formats():
    s = pd.Series(["01/15/2024", "02-20-2024", "bad"])
    dt = parse_purchase_date(s)
    assert str(dt.iloc[0].date()) == "2024-01-15"
    assert str(dt.iloc[1].date()) == "2024-02-20"
    assert pd.isna(dt.iloc[2])

def test_load_and_clean_adds_columns(tmp_path):
    # synthetic csv to avoid depending on repo data
    df = pd.DataFrame({
        "Customer_ID": [1,2],
        "Purchase_Amount": ["$100.00","$250.00"],
        "Time_of_Purchase": ["03/02/2024", "03-03-2024"]
    })
    p = tmp_path / "mini.csv"; df.to_csv(p, index=False)
    out = load_and_clean(p, save_processed=False)
    assert "Purchase_Amount_clean" in out
    assert "Purchase_Date" in out
    assert {"Purchase_Year","Purchase_Month","Purchase_Day","Purchase_DayOfWeek"}.issubset(out.columns)
