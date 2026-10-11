
"""Clean raw macroeconomic calendar data for analysis."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "macro_calendar_test.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "macro_calendar_clean.csv"

PLACEHOLDERS = ["&nbsp;", "nbsp", "N/A", "n/a", ""]


def clean_macro_data(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize calendar fields, timestamps, and surprise values."""
    cleaned = data.copy()

    # Normalize text and common missing-value placeholders.
    for column in cleaned.select_dtypes(include=["object", "str"]).columns:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace(
            r"(?i)^\s*(?:&nbsp;|nbsp|n/a)?\s*$",
            pd.NA,
            regex=True,
        )

    # Parse event dates without removing otherwise valid records yet.
    if "eventDate" in cleaned.columns:
        cleaned["eventDate"] = pd.to_datetime(
            cleaned["eventDate"], errors="coerce"
        )

    # Normalize numeric fields.
    numeric_columns = [
        "actualValue",
        "forecastValue",
        "previousValue",
        "surpriseVsForecast",
    ]

    for column in numeric_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(
                cleaned[column], errors="coerce"
            )

    # Normalize impact labels.
    if "impact" in cleaned.columns:
        cleaned["impact"] = cleaned["impact"].str.title()

    
    # Combine event date and GMT time into a UTC timestamp.
    if "eventDate" in cleaned.columns and "timeGmt" in cleaned.columns:
        date_text = pd.to_datetime(
            cleaned["eventDate"], errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        time_text = (
            cleaned["timeGmt"]
            .astype("string")
            .str.strip()
            .str.replace(r"\s*GMT$", "", regex=True, case=False)
        )

        timestamp_text = date_text + " " + time_text

        cleaned["eventTimestampUtc"] = pd.to_datetime(
            timestamp_text,
            format="%Y-%m-%d %H:%M",
            errors="coerce",
            utc=True,
        )


    # Calculate the surprise only when both values are available.
    if {"actualValue", "forecastValue"}.issubset(cleaned.columns):
        calculated_surprise = (
            cleaned["actualValue"] - cleaned["forecastValue"]
        )

        if "surpriseVsForecast" in cleaned.columns:
            cleaned["surpriseVsForecast"] = cleaned[
                "surpriseVsForecast"
            ].fillna(calculated_surprise)
        else:
            cleaned["surpriseVsForecast"] = calculated_surprise

    # Remove only records missing essential event identity fields.
    required = ["eventName", "eventDate"]
    for column in required:
        if column in cleaned.columns:
            cleaned = cleaned[cleaned[column].notna()]

    return cleaned.reset_index(drop=True)


def main() -> None:
    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw data file not found: {RAW_PATH}")

    raw = pd.read_csv(RAW_PATH)
    cleaned = clean_macro_data(raw)

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_PATH, index=False)

    print(f"Raw rows: {len(raw)}")
    print(f"Clean rows: {len(cleaned)}")
    print(f"Removed rows: {len(raw) - len(cleaned)}")
    print(f"Saved cleaned data to: {PROCESSED_PATH.relative_to(ROOT)}")

    if "actualValue" in cleaned.columns:
        print("Missing actual values:", cleaned["actualValue"].isna().sum())
    if "forecastValue" in cleaned.columns:
        print("Missing forecast values:", cleaned["forecastValue"].isna().sum())
    if "eventTimestampUtc" in cleaned.columns:
        print(
            "Invalid UTC timestamps:",
            cleaned["eventTimestampUtc"].isna().sum(),
        )
    if "surpriseVsForecast" in cleaned.columns:
        print(
            "Available surprise values:",
            cleaned["surpriseVsForecast"].notna().sum(),
        )


if __name__ == "__main__":
    main()
