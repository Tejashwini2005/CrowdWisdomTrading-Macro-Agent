
"""Download historical US macroeconomic indicators from FRED."""

import os
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FRED_API_KEY")
API_URL = "https://api.stlouisfed.org/fred/series/observations"

# Keep the initial dataset small and focused.
SERIES = {
    "UNRATE": "Unemployment Rate",
    "CPIAUCSL": "Consumer Price Index",
    "FEDFUNDS": "Federal Funds Rate",
    "PAYEMS": "Total Nonfarm Payrolls",
}

def fetch_series(series_id, series_name, start_date):
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "observation_start": start_date,
        "observation_end": date.today().isoformat(),
    }

    response = requests.get(API_URL, params=params, timeout=30)
    response.raise_for_status()

    observations = response.json().get("observations", [])

    return pd.DataFrame([
        {
            "date": item["date"],
            "series_id": series_id,
            "indicator": series_name,
            "value": (
                float(item["value"])
                if item["value"] not in ("", ".")
                else None
            ),
        }
        for item in observations
    ])

def main():
    if not API_KEY:
        raise RuntimeError("FRED_API_KEY is missing from .env")

    start_date = (date.today() - timedelta(days=180)).isoformat()
    frames = []

    for series_id, series_name in SERIES.items():
        try:
            frame = fetch_series(series_id, series_name, start_date)
            frames.append(frame)
            print(f"{series_id}: downloaded {len(frame)} observations")
        except requests.RequestException as exc:
            print(f"{series_id}: request failed ({type(exc).__name__})")

    if not frames:
        raise RuntimeError("No FRED data downloaded. Check the connection.")

    output = pd.concat(frames, ignore_index=True)
    output["date"] = pd.to_datetime(output["date"])
    output = output.sort_values(["date", "series_id"])

    output_path = Path("data/raw/fred_macro_data.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)

    print(f"\nSaved {len(output)} rows to {output_path}")
    print("Columns:", ", ".join(output.columns))
    print("Note: observation dates are not necessarily release dates.")

if __name__ == "__main__":
    main()
