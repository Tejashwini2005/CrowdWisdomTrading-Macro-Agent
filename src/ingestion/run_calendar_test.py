
"""Run a limited Apify calendar test and save the returned events."""

import sys
from pathlib import Path

import pandas as pd
import yaml

from src.ingestion.macro_calendar import fetch_macro_calendar


ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT / "config" / "config.yaml"
OUTPUT_PATH = ROOT / "data" / "raw" / "macro_calendar_test.csv"


def main():
    with CONFIG_PATH.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    settings = config["macro_calendar"]

    # Two-day test range; no more than 10 returned records.
    records = fetch_macro_calendar(
        actor_id=settings["actor_id"],
        date_from="2026-10-07",
        date_to="2026-10-08",
        countries=settings["countries"],
        impact_min=settings["impact_min"],
        max_results=min(settings["max_results_per_run"], 10),
    )

    if not records:
        print("The actor returned zero events for this test range.")
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(records).to_csv(OUTPUT_PATH, index=False)

    print(f"Records received: {len(records)}")
    print(f"Saved results to: {OUTPUT_PATH.relative_to(ROOT)}")
    print("Available fields:", ", ".join(records[0].keys()))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Calendar test failed: {type(exc).__name__}: {exc}")
        sys.exit(1)
