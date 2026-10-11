
import pandas as pd

from src.features.macro_features import create_macro_features


def test_calendar_features_are_created():
    data = pd.DataFrame({
        "eventDate": ["2026-10-07"],
        "impact": ["High"],
    })

    result = create_macro_features(data)

    assert result.loc[0, "day_of_week"] == "Wednesday"
    assert result.loc[0, "month"] == 10
    assert result.loc[0, "day_of_month"] == 7
    assert result.loc[0, "is_high_impact"] == 1


def test_surprise_uses_actual_minus_forecast():
    data = pd.DataFrame({
        "actualValue": [105.0, 98.0],
        "forecastValue": [100.0, 100.0],
    })

    result = create_macro_features(data)

    assert result.loc[0, "surprise"] == 5.0
    assert result.loc[1, "surprise"] == -2.0
    assert result["has_actual_and_forecast"].tolist() == [1, 1]


def test_missing_values_do_not_create_fake_surprises():
    data = pd.DataFrame({
        "actualValue": [None],
        "forecastValue": [100.0],
    })

    result = create_macro_features(data)

    assert pd.isna(result.loc[0, "surprise"])
    assert result.loc[0, "has_actual_and_forecast"] == 0
