

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = (
    PROJECT_ROOT / "data" / "processed" / "baseline_strategy_results.csv"
)
OUTPUT_FILE = PROJECT_ROOT / "reports" / "baseline_evaluation.txt"


def calculate_metrics(returns: pd.Series, periods: int = 252) -> dict:
    returns = returns.dropna().astype(float)

    if returns.empty:
        raise ValueError("No returns available for evaluation.")

    equity = (1 + returns).cumprod()
    total_return = equity.iloc[-1] - 1

    annualized_return = (
        equity.iloc[-1] ** (periods / len(returns)) - 1
        if equity.iloc[-1] > 0
        else np.nan
    )

    annualized_volatility = returns.std(ddof=1) * np.sqrt(periods)

    # Sharpe and Sortino use a zero risk-free rate for this baseline.
    sharpe = (
        returns.mean() / returns.std(ddof=1) * np.sqrt(periods)
        if returns.std(ddof=1) > 0
        else np.nan
    )

    downside_returns = returns[returns < 0]
    downside_deviation = np.sqrt((returns.clip(upper=0) ** 2).mean())

    sortino = (
        returns.mean() / downside_deviation * np.sqrt(periods)
        if downside_deviation > 0
        else np.nan
    )

    drawdown = equity / equity.cummax() - 1
    max_drawdown = drawdown.min()

    return {
        "Total return (%)": total_return * 100,
        "Annualized return (%)": annualized_return * 100,
        "Annualized volatility (%)": annualized_volatility * 100,
        "Sharpe ratio": sharpe,
        "Sortino ratio": sortino,
        "Maximum drawdown (%)": max_drawdown * 100,
    }


def calculate_trade_win_rate(df: pd.DataFrame) -> tuple[float, int]:
    """Calculate win rate from completed long-position trades."""
    position = df["position"].fillna(0).astype(int)
    returns = df["market_return"].fillna(0).astype(float)

    trade_returns = []
    current_trade_return = 1.0
    in_trade = False

    for i in range(len(df)):
        if position.iloc[i] == 1:
            if not in_trade:
                current_trade_return = 1.0
                in_trade = True

            current_trade_return *= 1 + returns.iloc[i]

            # A transition to cash closes the trade after this day's return.
            closes_trade = (
                i == len(df) - 1 or position.iloc[i + 1] == 0
            )
            if closes_trade:
                trade_returns.append(current_trade_return - 1)
                in_trade = False

    if not trade_returns:
        return float("nan"), 0

    win_rate = (
        sum(trade_return > 0 for trade_return in trade_returns)
        / len(trade_returns)
        * 100
    )
    return win_rate, len(trade_returns)


def main() -> None:
    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Results file not found: {INPUT_FILE}")

    df = pd.read_csv(INPUT_FILE, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)

    strategy_metrics = calculate_metrics(df["strategy_return"])
    benchmark_metrics = calculate_metrics(df["market_return"])
    win_rate, completed_trades = calculate_trade_win_rate(df)

    lines = [
        "BASELINE STRATEGY EVALUATION",
        f"Period: {df['Date'].min().date()} to {df['Date'].max().date()}",
        f"Observations: {len(df)}",
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
        f"Completed long trades: {completed_trades}",
        f"Trade win rate (%): {win_rate:.2f}",
        "",
        "Limitations:",
        "- Historical in-sample evaluation; not out-of-sample validation.",
        "- Zero risk-free rate assumed for Sharpe and Sortino ratios.",
        "- Transaction costs, slippage and taxes are excluded.",
        "- Results do not establish future profitability.",
    ])

    report = "\n".join(lines)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    print(report)
    print(f"\nReport saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
