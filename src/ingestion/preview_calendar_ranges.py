
"""Preview historical macro-calendar date ranges without API calls."""

import sys
from datetime import date, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.ingestion.date_ranges import split_date_range


def main() -> None:
    config_path = ROOT / "config" / "config.yaml"

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    historical_days = int(config["project"]["historical_days"])
    if historical_days < 1:
        raise ValueError("historical_days must be at least 1.")

    end = date.today()
    start = end - timedelta(days=historical_days - 1)

    ranges = split_date_range(start.isoformat(), end.isoformat())

    print(f"Historical window: {start} to {end}")
    print(f"Total days: {(end - start).days + 1}")
    print(f"Number of chunks: {len(ranges)}")

    for index, (date_from, date_to) in enumerate(ranges, start=1):
        print(f"{index}. {date_from} to {date_to}")


if __name__ == "__main__":
    main()
