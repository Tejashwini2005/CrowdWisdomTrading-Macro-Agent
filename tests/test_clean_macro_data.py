
import pandas as pd

from src.features.clean_macro_data import clean_macro_data


def test_clean_macro_data_removes_html_placeholders():
    data = pd.DataFrame({
        "eventName": ["CPI Release", "FOMC Speech"],
        "eventDate": ["2026-10-07", "2026-10-08"],
        "actual": ["3.2%", "&nbsp;"],
        "forecast": ["3.1%", None],
        "impact": ["high", "medium"],
    })

    cleaned = clean_macro_data(data)

    assert len(cleaned) == 2
    assert pd.isna(cleaned.loc[1, "actual"])
    assert cleaned.loc[0, "impact"] == "High"


def test_clean_macro_data_removes_invalid_dates():
    data = pd.DataFrame({
        "eventName": ["CPI Release", "Jobs Report"],
        "eventDate": ["2026-10-07", "not-a-date"],
    })

    cleaned = clean_macro_data(data)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["eventName"] == "CPI Release"


def test_clean_macro_data_removes_missing_event_names():
    data = pd.DataFrame({
        "eventName": ["CPI Release", None],
        "eventDate": ["2026-10-07", "2026-10-08"],
    })

    cleaned = clean_macro_data(data)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["eventName"] == "CPI Release"
