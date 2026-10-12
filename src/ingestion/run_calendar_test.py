"""Preview historical macro-calendar ranges without making API calls."""

import sys
from datetime import date, timedelta
from pathlib import Path


import yaml

from src.ingestion.date_ranges import split_date_range

ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "config.yaml"
OUTPUT_PATH = ROOT / "data" / "raw" / "macro_calendar_test.csv"


def main():
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    project_settings = config["project"]
    historical_days = int(project_settings["historical_days"])
    if historical_days < 1:
        raise ValueError("historical_days must be at least 1.")

    end = date.today()
    start = end - timedelta(days=historical_days - 1)
    chunks = split_date_range(start.isoformat(), end.isoformat())

    print(f"Historical window: {start} to {end}")
    print(f"Total days: {historical_days}")
    print(f"Date chunks: {len(chunks)}")
    print(
    "NOTE: This script is preview-only and makes no API requests. "
    "A future live fetch would be limited to 10 events per run on "
    "the free plan and may return incomplete historical coverage."
)
    print("Planned chunks:")
    for index, (date_from, date_to) in enumerate(chunks, start=1):
        print(f"{index}. {date_from} to {date_to}")

    # Deliberately do not fetch data automatically.
    # Enable a live run only after reviewing cost and coverage limits.
    print("Preview only. No API requests were made.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Calendar preview failed: {type(exc).__name__}: {exc}")
        sys.exit(1)
