


from pathlib import Path

import pandas as pd
import yfinance as yf


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "spy_historical_prices.csv"


def download_market_data(
    ticker: str = "SPY",
    period: str = "2y",
) -> pd.DataFrame:
    """Download daily market data and save it as a CSV file."""
    print(f"Downloading historical data for {ticker}...")

    data = yf.download(
        ticker,
        period=period,
        interval="1d",
        auto_adjust=True,
        progress=False,
        threads=False,
    )

    if data.empty:
        raise RuntimeError(
            "No market data was returned. Check your internet connection "
            "and try again later."
        )

    # Handle both single-level and multi-level column formats.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data.index.name = "Date"
    data = data.reset_index()

    required_columns = {"Date", "Open", "High", "Low", "Close", "Volume"}
    missing_columns = required_columns.difference(data.columns)

    if missing_columns:
        raise ValueError(
            f"Downloaded data is missing columns: {sorted(missing_columns)}"
        )

    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data = data.dropna(subset=["Date", "Close"])
    data = data.sort_values("Date").drop_duplicates(subset=["Date"])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(OUTPUT_FILE, index=False)

    print(f"Saved {len(data)} daily records to:")
    print(OUTPUT_FILE)
    print("\nFirst five rows:")
    print(data.head().to_string(index=False))
    print("\nLast available date:", data["Date"].max().date())

    return data


if __name__ == "__main__":
    download_market_data()
