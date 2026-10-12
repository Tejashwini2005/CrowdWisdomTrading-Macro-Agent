"""Run the local CrowdWisdomTrading pipeline without live API ingestion."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

STAGES = [
    ("Clean macro calendar", "src.features.clean_macro_data"),
    ("Build macro features", "src.features.macro_features"),
    ("Clean macro news", "src.features.clean_macro_news"),
    ("Analyze news sentiment", "src.features.news_sentiment"),
    ("Build daily news features", "src.features.daily_news_features"),
    ("Run baseline strategy", "src.models.baseline_strategy"),
    ("Evaluate baseline strategy", "src.validation.evaluate_strategy"),
    ("Run walk-forward validation", "src.validation.walk_forward_validation"),
    ("Run strategy permutation model", "src.models.strategy_permutation_model"),
]

CHART_MODULE = "src.visualization.strategy_charts"

REQUIRED_INPUTS = [
    Path("data/raw/macro_calendar_test.csv"),
    Path("data/raw/macro_news_combined.csv"),
    Path("data/raw/spy_historical_prices.csv"),
]


def check_inputs() -> list[Path]:
    """Return required input files that are missing or empty."""
    return [
        path
        for path in REQUIRED_INPUTS
        if not (PROJECT_ROOT / path).is_file()
        or (PROJECT_ROOT / path).stat().st_size == 0
    ]


def run_stage(label: str, module: str) -> None:
    """Run one project module and stop if it fails."""
    print(f"\n{'=' * 65}")
    print(f"STEP: {label}")
    print(f"MODULE: {module}")
    print("=" * 65)

    subprocess.run(
        [sys.executable, "-m", module],
        cwd=PROJECT_ROOT,
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the local macro trading research pipeline."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned stages without running them.",
    )
    args = parser.parse_args()

    print("CrowdWisdomTrading Macro Economics Agent")
    print("Mode:", "DRY RUN" if args.dry_run else "LOCAL PIPELINE")
    print("Live API ingestion is disabled in this entry point.")

    if args.dry_run:
        for number, (label, module) in enumerate(STAGES, start=1):
            print(f"{number}. {label}: python -m {module}")
        print(f"{len(STAGES) + 1}. Generate charts, if their inputs exist")
        return 0

    missing = check_inputs()
    if missing:
        print("\nERROR: Required input files are missing or empty:")
        for path in missing:
            print(f" - {path}")
        print("\nNo pipeline stages were started.")
        return 1

    try:
        for label, module in STAGES:
            run_stage(label, module)

        chart_inputs = [
            Path("data/processed/baseline_holdout_results.csv"),
            Path("data/processed/walk_forward_folds.csv"),
            Path("data/processed/strategy_permutation_summary.csv"),
        ]
        missing_chart_inputs = [
            path
            for path in chart_inputs
            if not (PROJECT_ROOT / path).is_file()
            or (PROJECT_ROOT / path).stat().st_size == 0
        ]

        if missing_chart_inputs:
            print("\nCharts skipped: required chart inputs are missing or empty.")
            for path in missing_chart_inputs:
                print(f" - {path}")
        else:
            run_stage("Generate strategy charts", CHART_MODULE)

    except subprocess.CalledProcessError as exc:
        print(f"\nERROR: Pipeline stopped because {exc.cmd} failed.")
        return exc.returncode or 1

    print("\nLocal pipeline finished.")
    print("Review reports and data-quality limitations before interpreting results.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
