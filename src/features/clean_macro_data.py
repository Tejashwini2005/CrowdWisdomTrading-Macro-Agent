
"""Clean raw macroeconomic calendar data for analysis."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
RAW_PATH = ROOT / "data" / "raw" / "macro_calendar_test.csv"
PROCESSED_PATH = ROOT / "data" / "processed" / "macro_calendar_clean.csv"

PLACEHOLDERS = ["&nbsp;", "nbsp", "N/A", "n/a", ""]


def clean_macro_data(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize missing values and data types in macro calendar records."""
    cleaned = data.copy()

    # Remove whitespace and HTML placeholder values.
    for column in cleaned.select_dtypes(include=["object", "str"]).columns:
        cleaned[column] = cleaned[column].replace(
            r"^\s*(?:&nbsp;|nbsp|N/A)?\s*$",
            pd.NA,
            regex=True,
        )
        cleaned[column] = cleaned[column].astype("string").str.strip()

    # Parse dates; invalid dates become missing.
    if "eventDate" in cleaned.columns:
        cleaned["eventDate"] = pd.to_datetime(
            cleaned["eventDate"], errors="coerce"
        )

    # Convert numeric output fields while preserving original text fields.
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

    # Exclude records without an event name or valid event date.
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

    if "actual" in cleaned.columns:
        print("Missing actual values:", cleaned["actual"].isna().sum())
    if "forecast" in cleaned.columns:
        print("Missing forecast values:", cleaned["forecast"].isna().sum())


if __name__ == "__main__":
    main()
