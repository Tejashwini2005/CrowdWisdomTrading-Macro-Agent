

from pathlib import Path

import pandas as pd

from src.validation.evaluate_strategy import calculate_metrics


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "baseline_strategy_results.csv"
)
OUTPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "baseline_holdout_results.csv"
)
REPORT_FILE = PROJECT_ROOT / "reports" / "walk_forward_evaluation.txt"


def main() -> None:
    df = pd.read_csv(INPUT_FILE, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    if len(df) < 100:
        raise ValueError("Not enough observations for chronological validation.")

    # Reserve the final 30% as unseen holdout data.
    split_index = int(len(df) * 0.70)
    development = df.iloc[:split_index].copy()
    holdout = df.iloc[split_index:].copy()

    if holdout.empty:
        raise ValueError("The holdout period is empty.")

    # Indicators and signals were computed causally from historical data.
    # Do not tune strategy parameters using holdout results.
    holdout["strategy_equity"] = (
        1 + holdout["strategy_return"]
    ).cumprod()
    holdout["buy_hold_equity"] = (
        1 + holdout["market_return"]
    ).cumprod()

    holdout.to_csv(OUTPUT_FILE, index=False)

    strategy_metrics = calculate_metrics(holdout["strategy_return"])
    benchmark_metrics = calculate_metrics(holdout["market_return"])

    lines = [
        "CHRONOLOGICAL HOLDOUT EVALUATION",
        "",
        f"Development period: {development['Date'].min().date()} "
        f"to {development['Date'].max().date()}",
        f"Development observations: {len(development)}",
        "",
        f"Holdout period: {holdout['Date'].min().date()} "
        f"to {holdout['Date'].max().date()}",
        f"Holdout observations: {len(holdout)}",
        "",
        "METRIC | STRATEGY | BUY AND HOLD",
    ]

    for metric in strategy_metrics:
        lines.append(
            f"{metric} | {strategy_metrics[metric]:.2f} "
            f"| {benchmark_metrics[metric]:.2f}"
        )

    lines.extend([
        "",
        "Methodology and limitations:",
        "- Chronological 70% development / 30% holdout split.",
        "- Moving-average rules remain fixed; no holdout tuning.",
        "- Moving averages use current and past closing prices only.",
        "- Positions are shifted by one trading day.",
        "- Transaction costs, slippage and taxes are excluded.",
        "- Holdout performance is historical and may not generalize.",
        "- This is a single holdout test, not rolling walk-forward validation.",
    ])

    report = "\n".join(lines)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")

    print(report)
    print(f"\nHoldout data saved to: {OUTPUT_FILE}")
    print(f"Evaluation report saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
