
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "spy_historical_prices.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed" / "baseline_strategy_results.csv"


def run_baseline_strategy() -> pd.DataFrame:
    df = pd.read_csv(INPUT_FILE, parse_dates=["Date"])
    df = df.sort_values("Date").drop_duplicates("Date").reset_index(drop=True)

    # Calculate trend indicators using current and past closing prices.
    df["ma_20"] = df["Close"].rolling(window=20).mean()
    df["ma_50"] = df["Close"].rolling(window=50).mean()

    # A signal is determined at the end of each trading day.
    df["signal"] = (df["ma_20"] > df["ma_50"]).astype(int)

    # Apply the signal one trading day later to avoid look-ahead bias.
    df["position"] = df["signal"].shift(1).fillna(0).astype(int)

    # Close-to-close return for each trading day.
    df["market_return"] = df["Close"].pct_change().fillna(0)

    # Strategy earns the market return only when already holding SPY.
    df["strategy_return"] = df["position"] * df["market_return"]

    # Compound returns to track strategy and buy-and-hold growth.
    df["strategy_equity"] = (1 + df["strategy_return"]).cumprod()
    df["buy_hold_equity"] = (1 + df["market_return"]).cumprod()

    # Save the detailed daily results.
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved strategy results to: {OUTPUT_FILE}")
    print(f"Trading days: {len(df)}")
    print(f"Days holding SPY: {df['position'].sum()}")
    print(f"Strategy cumulative return: {(df['strategy_equity'].iloc[-1] - 1) * 100:.2f}%")
    print(f"Buy-and-hold cumulative return: {(df['buy_hold_equity'].iloc[-1] - 1) * 100:.2f}%")

    return df


if __name__ == "__main__":
    run_baseline_strategy()
