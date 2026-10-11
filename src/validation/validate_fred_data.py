
"""Validate the downloaded FRED macroeconomic dataset."""

from pathlib import Path

import pandas as pd

INPUT_FILE = Path("data/raw/fred_macro_data.csv")
REPORT_FILE = Path("reports/fred_data_quality.txt")

EXPECTED_SERIES = {
    "UNRATE",
    "CPIAUCSL",
    "FEDFUNDS",
    "PAYEMS",
}

def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Missing input file: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    missing_dates = int(df["date"].isna().sum())
    missing_values = int(df["value"].isna().sum())
    duplicate_rows = int(df.duplicated(["date", "series_id"]).sum())

    present_series = set(df["series_id"].dropna().unique())
    missing_series = EXPECTED_SERIES - present_series

    checks = {
        "File exists": True,
        "Dataset is not empty": not df.empty,
        "All expected indicators present": not missing_series,
        "No invalid dates": missing_dates == 0,
        "No missing numeric values": missing_values == 0,
        "No duplicate date/indicator pairs": duplicate_rows == 0,
    }

    lines = [
        "FRED MACROECONOMIC DATA QUALITY REPORT",
        "=" * 40,
        f"Input file: {INPUT_FILE}",
        f"Total rows: {len(df)}",
        f"Date range: {df['date'].min()} to {df['date'].max()}",
        f"Missing dates: {missing_dates}",
        f"Missing numeric values: {missing_values}",
        f"Duplicate date/indicator pairs: {duplicate_rows}",
        f"Missing expected indicators: {sorted(missing_series)}",
        "",
        "Observations by indicator:",
    ]

    counts = df.groupby("series_id").size()
    lines.extend(f"- {series}: {count}" for series, count in counts.items())

    lines.append("")
    lines.append("Validation checks:")
    lines.extend(
        f"- {'PASS' if passed else 'FAIL'}: {name}"
        for name, passed in checks.items()
    )

    lines.extend([
        "",
        "LIMITATIONS",
        "- Observation dates are not necessarily public release dates.",
        "- Historical values may be revised.",
        "- FRED data do not provide consensus forecasts in this dataset.",
        "- Passing data checks does not establish predictive trading value.",
    ])

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("\n".join(lines))
    print(f"\nReport saved to: {REPORT_FILE}")

    if not all(checks.values()):
        raise SystemExit("Validation failed. Review the report.")

if __name__ == "__main__":
    main()
