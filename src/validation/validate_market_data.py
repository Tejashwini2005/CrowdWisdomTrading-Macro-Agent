

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "data" / "raw" / "spy_historical_prices.csv"


def validate_market_data() -> bool:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Market data not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

    required_columns = [
        "Date", "Open", "High", "Low", "Close", "Volume"
    ]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    print(f"Total rows: {len(df)}")
    print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
    print(f"Duplicate dates: {df['Date'].duplicated().sum()}")

    numeric_columns = ["Open", "High", "Low", "Close", "Volume"]
    print("\nMissing values:")
    print(df[required_columns].isna().sum().to_string())

    print("\nNon-positive prices:")
    print((df[["Open", "High", "Low", "Close"]] <= 0).sum().to_string())

    print("\nPrice relationship checks:")
    print(f"High below Low: {(df['High'] < df['Low']).sum()}")
    print(f"Close above High: {(df['Close'] > df['High']).sum()}")
    print(f"Close below Low: {(df['Close'] < df['Low']).sum()}")

    valid = (
        not df.empty
        and not df[required_columns].isna().any().any()
        and not df["Date"].duplicated().any()
        and (df[numeric_columns] >= 0).all().all()
        and (df[["Open", "High", "Low", "Close"]] > 0).all().all()
        and (df["High"] >= df["Low"]).all()
        and (df["Close"] <= df["High"]).all()
        and (df["Close"] >= df["Low"]).all()
        and df["Date"].is_monotonic_increasing
    )

    print(f"\nValidation result: {'PASSED' if valid else 'FAILED'}")
    return bool(valid)


if __name__ == "__main__":
    if not validate_market_data():
        raise SystemExit(1)
