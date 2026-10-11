
"""Create time and event features from cleaned macroeconomic data."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "processed" / "macro_calendar_clean.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "macro_features.csv"


def create_macro_features(data: pd.DataFrame) -> pd.DataFrame:
    """Add timestamp, calendar, impact, and surprise features."""
    featured = data.copy()

    # Prefer the validated UTC timestamp for time-based features.
    if "eventTimestampUtc" in featured.columns:
        timestamps = pd.to_datetime(
            featured["eventTimestampUtc"], errors="coerce", utc=True
        )
    elif "eventDate" in featured.columns:
        timestamps = pd.to_datetime(
            featured["eventDate"], errors="coerce", utc=True
        )
    else:
        timestamps = pd.Series(
            pd.NaT, index=featured.index, dtype="datetime64[ns, UTC]"
        )

    featured["event_timestamp_utc"] = timestamps
    featured["day_of_week"] = timestamps.dt.day_name()
    featured["month"] = timestamps.dt.month
    featured["day_of_month"] = timestamps.dt.day
    featured["hour_utc"] = timestamps.dt.hour

    # Encode event impact without treating missing impact as high/low.
    if "impact" in featured.columns:
        impact = featured["impact"].astype("string").str.strip().str.lower()
        featured["is_high_impact"] = (
            impact.eq("high").fillna(False).astype("int8")
        )
        featured["impact_missing"] = impact.isna().astype("int8")

    # Calculate numeric surprises only when both values are available.
    if {"actualValue", "forecastValue"}.issubset(featured.columns):
        actual = pd.to_numeric(featured["actualValue"], errors="coerce")
        forecast = pd.to_numeric(featured["forecastValue"], errors="coerce")

        valid_pair = actual.notna() & forecast.notna()
        featured["surprise"] = (actual - forecast).where(valid_pair)
        featured["has_actual_and_forecast"] = valid_pair.astype("int8")

        # Relative surprise is descriptive only; avoid division by zero.
        valid_denominator = forecast.notna() & forecast.ne(0)
        featured["relative_surprise_pct"] = (
            ((actual - forecast) / forecast.abs()) * 100
        ).where(valid_pair & valid_denominator)

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
    print("Valid UTC timestamps:", featured["event_timestamp_utc"].notna().sum())
    if "has_actual_and_forecast" in featured.columns:
        print(
            "Events with actual and forecast:",
            featured["has_actual_and_forecast"].sum(),
        )
    print("Added time, impact, surprise, and relative-surprise features.")


if __name__ == "__main__":
    main()
