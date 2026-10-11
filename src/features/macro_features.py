
"""Create time and event features from cleaned macroeconomic data."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "processed" / "macro_calendar_clean.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "macro_features.csv"


def create_macro_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add calendar features and numeric surprise features."""
    featured = data.copy()

    if "eventDate" in featured.columns:
        dates = pd.to_datetime(featured["eventDate"], errors="coerce")
        featured["day_of_week"] = dates.dt.day_name()
        featured["month"] = dates.dt.month
        featured["day_of_month"] = dates.dt.day

    if "impact" in featured.columns:
        featured["is_high_impact"] = (
            featured["impact"].astype("string").str.lower() == "high"
        ).astype("int8")

    if {"actualValue", "forecastValue"}.issubset(featured.columns):
        actual = pd.to_numeric(featured["actualValue"], errors="coerce")
        forecast = pd.to_numeric(featured["forecastValue"], errors="coerce")

        featured["surprise"] = actual - forecast
        featured["has_actual_and_forecast"] = (
            actual.notna() & forecast.notna()
        ).astype("int8")

    return featured


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned data not found: {INPUT_PATH}. "
            "Run the cleaning step first."
        )

    data = pd.read_csv(INPUT_PATH)
    featured = create_macro_features(data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    featured.to_csv(OUTPUT_PATH, index=False)

    print(f"Input rows: {len(data)}")
    print(f"Output rows: {len(featured)}")
    print(f"Saved features to: {OUTPUT_PATH.relative_to(ROOT)}")
    print("Feature columns added when source fields are available:")
    print("day_of_week, month, day_of_month, is_high_impact, surprise")


if __name__ == "__main__":
    main()
