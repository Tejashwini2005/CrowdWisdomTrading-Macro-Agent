
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import TimeSeriesSplit


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "spy_historical_prices.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
RESULTS_FILE = OUTPUT_DIR / "strategy_permutation_predictions.csv"
METRICS_FILE = PROJECT_ROOT / "reports" / "ml_strategy_evaluation.txt"

# Candidate configurations to compare.
STRATEGIES = [(5, 20), (10, 30), (20, 50), (20, 100), (50, 100)]


def build_dataset(prices: pd.DataFrame) -> pd.DataFrame:
    """Create lagged market features and next-day strategy-return targets."""
    df = prices.copy()
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values("Date").drop_duplicates("Date").reset_index(drop=True)

    df["market_return"] = df["Close"].pct_change()
    df["return_lag_1"] = df["market_return"].shift(1)
    df["return_lag_5"] = df["Close"].pct_change(5).shift(1)
    df["volatility_20"] = df["market_return"].rolling(20).std().shift(1)
    df["momentum_20"] = df["Close"].pct_change(20).shift(1)

    frames = []
    for short_window, long_window in STRATEGIES:
        item = df.copy()
        item["short_window"] = short_window
        item["long_window"] = long_window
        item["ma_short"] = item["Close"].rolling(short_window).mean()
        item["ma_long"] = item["Close"].rolling(long_window).mean()

        # Signal from the previous close is held for the next trading day.
        item["position"] = (
            (item["ma_short"] > item["ma_long"]).astype(int).shift(1)
        )
        item["target_return"] = item["position"] * item["market_return"]

        frames.append(item)

    combined = pd.concat(frames, ignore_index=True)
    combined["ma_gap"] = (
        combined["ma_short"] / combined["ma_long"] - 1
    )

    features = [
        "short_window",
        "long_window",
        "return_lag_1",
        "return_lag_5",
        "volatility_20",
        "momentum_20",
        "ma_gap",
    ]
    combined = combined.replace([np.inf, -np.inf], np.nan)
    combined = combined.dropna(subset=features + ["target_return"])
    return combined


def main() -> None:
    prices = pd.read_csv(INPUT_FILE)
    dataset = build_dataset(prices)

    feature_columns = [
        "short_window",
        "long_window",
        "return_lag_1",
        "return_lag_5",
        "volatility_20",
        "momentum_20",
        "ma_gap",
    ]

    # Split by unique dates, never by shuffled rows.
    dates = np.sort(dataset["Date"].unique())
    if len(dates) < 100:
        raise ValueError("Not enough dates for chronological model evaluation.")

    split_index = int(len(dates) * 0.8)
    train_dates = dates[:split_index]
    test_dates = dates[split_index:]

    train = dataset[dataset["Date"].isin(train_dates)].copy()
    test = dataset[dataset["Date"].isin(test_dates)].copy()

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=5,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
    )
    model.fit(train[feature_columns], train["target_return"])
    test["predicted_return"] = model.predict(test[feature_columns])

    mae = mean_absolute_error(test["target_return"], test["predicted_return"])
    rmse = np.sqrt(mean_squared_error(test["target_return"], test["predicted_return"]))

    # Per-configuration metrics on the held-out dates.
    summaries = []
    for (short_window, long_window), group in test.groupby(
        ["short_window", "long_window"]
    ):
        actual = group["target_return"]
        predicted = group["predicted_return"]

        # This is a model-selection illustration, not a live trading signal.
        summaries.append(
            {
                "short_window": short_window,
                "long_window": long_window,
                "test_days": len(group),
                "actual_total_return_pct": ((1 + actual).prod() - 1) * 100,
                "predicted_mean_daily_return_pct": predicted.mean() * 100,
                "actual_mean_daily_return_pct": actual.mean() * 100,
                "prediction_mae": mean_absolute_error(actual, predicted),
            }
        )

    summary = pd.DataFrame(summaries).sort_values(
        "predicted_mean_daily_return_pct", ascending=False
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_FILE.parent.mkdir(parents=True, exist_ok=True)
    test[
        [
            "Date",
            "short_window",
            "long_window",
            "target_return",
            "predicted_return",
        ]
    ].to_csv(RESULTS_FILE, index=False)
    summary.to_csv(OUTPUT_DIR / "strategy_permutation_summary.csv", index=False)

    # Sequential folds provide additional out-of-sample error checks.
    fold_errors = []
    date_index = pd.Index(dataset["Date"].drop_duplicates().sort_values())
    splitter = TimeSeriesSplit(n_splits=5)

    for fold_number, (train_idx, test_idx) in enumerate(
        splitter.split(date_index), start=1
    ):
        fold_train_dates = date_index[train_idx]
        fold_test_dates = date_index[test_idx]
        fold_train = dataset[dataset["Date"].isin(fold_train_dates)]
        fold_test = dataset[dataset["Date"].isin(fold_test_dates)]

        fold_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=5,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=-1,
        )
        fold_model.fit(fold_train[feature_columns], fold_train["target_return"])
        fold_predictions = fold_model.predict(fold_test[feature_columns])

        fold_errors.append(
            {
                "fold": fold_number,
                "test_start": fold_test["Date"].min().date(),
                "test_end": fold_test["Date"].max().date(),
                "mae": mean_absolute_error(
                    fold_test["target_return"], fold_predictions
                ),
                "rmse": np.sqrt(
                    mean_squared_error(
                        fold_test["target_return"], fold_predictions
                    )
                ),
            }
        )

    with METRICS_FILE.open("w", encoding="utf-8") as report:
        report.write("ML STRATEGY-PERMUTATION EVALUATION\n\n")
        report.write(f"Source: {INPUT_FILE.name}\n")
        report.write(f"Configurations: {STRATEGIES}\n")
        report.write(f"Unique dates: {len(dates)}\n")
        report.write(
            f"Training dates: {train['Date'].min().date()} to "
            f"{train['Date'].max().date()}\n"
        )
        report.write(
            f"Test dates: {test['Date'].min().date()} to "
            f"{test['Date'].max().date()}\n\n"
        )
        report.write(f"Holdout MAE (daily return): {mae:.6f}\n")
        report.write(f"Holdout RMSE (daily return): {rmse:.6f}\n\n")
        report.write("Per-configuration holdout summary:\n")
        report.write(summary.to_string(index=False))
        report.write("\n\nFive-fold chronological error checks:\n")
        report.write(pd.DataFrame(fold_errors).to_string(index=False))
        report.write(
            "\n\nLimitations:\n"
            "- This is a small historical SPY dataset.\n"
            "- Predictions are estimates, not guaranteed returns or profitability.\n"
            "- No transaction costs, slippage, taxes, or market impact are included.\n"
            "- Strategy rankings may change across market regimes.\n"
            "- Macro event and news features are not included in this model yet.\n"
        )

    print("ML strategy-permutation model completed.")
    print(f"Training rows: {len(train)} | Test rows: {len(test)}")
    print(f"Holdout MAE: {mae:.6f}")
    print(f"Holdout RMSE: {rmse:.6f}")
    print("\nHoldout configuration summary:")
    print(summary.to_string(index=False))
    print(f"\nPredictions saved to: {RESULTS_FILE}")
    print(f"Summary saved to: {OUTPUT_DIR / 'strategy_permutation_summary.csv'}")
    print(f"Evaluation report saved to: {METRICS_FILE}")


if __name__ == "__main__":
    main()
