
"""Five-split expanding-window evaluation of the fixed baseline strategy."""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import TimeSeriesSplit

from src.validation.evaluate_strategy import calculate_metrics


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "processed" / "baseline_strategy_results.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
FOLDS_FILE = OUTPUT_DIR / "walk_forward_folds.csv"
REPORT_FILE = PROJECT_ROOT / "reports" / "walk_forward_evaluation.txt"


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Results file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE, parse_dates=["Date"])
    df = df.sort_values("Date").drop_duplicates("Date").reset_index(drop=True)

    required = {"Date", "strategy_return", "market_return"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if len(df) < 100:
        raise ValueError("Not enough observations for five-split validation.")

    # Each test window follows its training window in chronological order.
    splitter = TimeSeriesSplit(n_splits=5)
    fold_rows = []
    report_lines = [
        "FIVE-SPLIT EXPANDING-WINDOW WALK-FORWARD EVALUATION",
        "",
        f"Dataset period: {df['Date'].min().date()} to {df['Date'].max().date()}",
        f"Total observations: {len(df)}",
        "Strategy: fixed 20-day / 50-day moving-average rule",
        "Benchmark: buy and hold",
        "Risk-free rate: 0%",
        "Transaction costs and slippage: excluded",
        "",
    ]

    for fold_number, (train_idx, test_idx) in enumerate(
        splitter.split(df), start=1
    ):
        train = df.iloc[train_idx]
        test = df.iloc[test_idx].copy()

        # Metrics are calculated only on this fold's unseen test window.
        strategy_metrics = calculate_metrics(test["strategy_return"])
        benchmark_metrics = calculate_metrics(test["market_return"])

        fold_rows.append({
            "fold": fold_number,
            "train_start": train["Date"].min().date(),
            "train_end": train["Date"].max().date(),
            "train_observations": len(train),
            "test_start": test["Date"].min().date(),
            "test_end": test["Date"].max().date(),
            "test_observations": len(test),
            **{f"strategy_{k}": v for k, v in strategy_metrics.items()},
            **{f"benchmark_{k}": v for k, v in benchmark_metrics.items()},
        })

        report_lines.extend([
            f"FOLD {fold_number}",
            f"Training: {train['Date'].min().date()} to "
            f"{train['Date'].max().date()} ({len(train)} observations)",
            f"Testing:  {test['Date'].min().date()} to "
            f"{test['Date'].max().date()} ({len(test)} observations)",
            "Metric | Strategy | Buy and hold",
        ])

        for metric in strategy_metrics:
            report_lines.append(
                f"{metric} | {strategy_metrics[metric]:.3f} "
                f"| {benchmark_metrics[metric]:.3f}"
            )
        report_lines.append("")

    folds = pd.DataFrame(fold_rows)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    folds.to_csv(FOLDS_FILE, index=False)

    # Summary is the mean of fold-level metrics, not a compounded portfolio.
    metric_names = list(calculate_metrics(df["strategy_return"]).keys())
    report_lines.extend([
        "MEAN OF FIVE TEST-FOLD METRICS",
        "(Descriptive average; not a single compounded return series.)",
    ])

    for metric in metric_names:
        strategy_col = f"strategy_{metric}"
        benchmark_col = f"benchmark_{metric}"
        report_lines.append(
            f"{metric} | {folds[strategy_col].mean():.3f} "
            f"| {folds[benchmark_col].mean():.3f}"
        )

    report_lines.extend([
        "",
        "LIMITATIONS",
        "- The moving-average strategy is fixed, not retrained per fold.",
        "- This evaluates the fixed strategy on five sequential test windows.",
        "- It does not yet satisfy the separate ML strategy-permutation requirement.",
        "- No transaction costs, slippage, taxes, or market-impact costs.",
        "- Historical results do not guarantee future performance.",
    ])

    report = "\n".join(report_lines)
    REPORT_FILE.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nFold data saved to: {FOLDS_FILE}")
    print(f"Report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
