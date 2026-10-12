
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"
OUTPUT_DIR = ROOT / "reports" / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def plot_holdout_equity():
    """Compare normalized strategy and buy-and-hold equity."""
    df = pd.read_csv(DATA_DIR / "baseline_holdout_results.csv")
    df["Date"] = pd.to_datetime(df["Date"])

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(df["Date"], df["strategy_equity"], label="Moving-average strategy")
    ax.plot(df["Date"], df["buy_hold_equity"], label="Buy and hold")

    ax.set_title("SPY Holdout Equity: Strategy vs Buy and Hold")
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalized equity (starting value = 1)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "holdout_equity_comparison.png", dpi=160)
    plt.close(fig)


def plot_walk_forward():
    """Compare strategy and benchmark returns for each test fold."""
    df = pd.read_csv(DATA_DIR / "walk_forward_folds.csv")
    x = range(len(df))
    width = 0.36

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(
        [i - width / 2 for i in x],
        df["strategy_Total return (%)"],
        width,
        label="Strategy",
    )
    ax.bar(
        [i + width / 2 for i in x],
        df["benchmark_Total return (%)"],
        width,
        label="Buy-and-hold benchmark",
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels([f"Fold {n}" for n in df["fold"]])
    ax.set_title("Walk-Forward Test-Fold Returns")
    ax.set_xlabel("Chronological test fold")
    ax.set_ylabel("Total return (%)")
    ax.axhline(0, linewidth=0.8)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "walk_forward_returns.png", dpi=160)
    plt.close(fig)


def plot_configuration_returns():
    """Show actual holdout returns for tested moving-average configurations."""
    df = pd.read_csv(DATA_DIR / "strategy_permutation_summary.csv")
    df = df.sort_values(["short_window", "long_window"]).copy()

    labels = [
        f"{int(row.short_window)}/{int(row.long_window)}"
        for row in df.itertuples()
    ]

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(
        labels,
        df["actual_total_return_pct"],
    )

    for bar, value in zip(bars, df["actual_total_return_pct"]):
        offset = 0.08 if value >= 0 else -0.15
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + offset,
            f"{value:.2f}%",
            ha="center",
            va="bottom" if value >= 0 else "top",
            fontsize=9,
        )

    ax.set_title("Actual Holdout Return by Moving-Average Configuration")
    ax.set_xlabel("Short / long moving-average windows")
    ax.set_ylabel("Actual holdout total return (%)")
    ax.axhline(0, linewidth=0.8)
    ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / "configuration_holdout_returns.png", dpi=160)
    plt.close(fig)


def main():
    plot_holdout_equity()
    plot_walk_forward()
    plot_configuration_returns()

    print("Strategy charts saved to:", OUTPUT_DIR)
    for name in (
        "holdout_equity_comparison.png",
        "walk_forward_returns.png",
        "configuration_holdout_returns.png",
    ):
        path = OUTPUT_DIR / name
        print(f"{name}: {path.stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
