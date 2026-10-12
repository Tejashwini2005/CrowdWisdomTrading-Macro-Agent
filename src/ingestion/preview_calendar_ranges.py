"""Preview historical macro-calendar date ranges without API calls."""

import sys
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.ingestion.date_ranges import split_date_range


def main() -> None:
    end = date.today()
    start = end - timedelta(days=179)

    ranges = split_date_range(start.isoformat(), end.isoformat())

    print(f"Historical window: {start} to {end}")
    print(f"Total days: {(end - start).days + 1}")
    print(f"Number of chunks: {len(ranges)}")

    for index, (date_from, date_to) in enumerate(ranges, start=1):
        print(f"{index}. {date_from} to {date_to}")


if __name__ == "__main__":
    main()