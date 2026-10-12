"""Aggregate dated news sentiment into daily features."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "processed" / "macro_news_sentiment.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "daily_news_features.csv"


def create_daily_news_features(data: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sentiment by UTC publication date."""
    required = {"published_date", "sentiment_score", "sentiment_label"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    featured = data.copy()
    featured["published_date"] = pd.to_datetime(
        featured["published_date"], errors="coerce", utc=True
    )
    featured["sentiment_score"] = pd.to_numeric(
        featured["sentiment_score"], errors="coerce"
    )

    # Articles without a publication date cannot be assigned to a day.
    featured = featured.dropna(
        subset=["published_date", "sentiment_score"]
    ).copy()

    featured["date"] = featured["published_date"].dt.strftime("%Y-%m-%d")

    daily = (
        featured.groupby("date", as_index=False)
        .agg(
            article_count=("sentiment_score", "size"),
            mean_sentiment=("sentiment_score", "mean"),
            total_sentiment=("sentiment_score", "sum"),
            positive_articles=(
                "sentiment_label",
                lambda values: values.eq("positive").sum(),
            ),
            neutral_articles=(
                "sentiment_label",
                lambda values: values.eq("neutral").sum(),
            ),
            negative_articles=(
                "sentiment_label",
                lambda values: values.eq("negative").sum(),
            ),
        )
        .sort_values("date")
        .reset_index(drop=True)
    )

    return daily


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Sentiment data not found: {INPUT_PATH}. "
            "Run the sentiment scoring step first."
        )

    data = pd.read_csv(INPUT_PATH)
    daily = create_daily_news_features(data)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    daily.to_csv(OUTPUT_PATH, index=False)

    print(f"Input articles: {len(data)}")
    print(f"Articles with usable dates and scores: {daily['article_count'].sum()}")
    print(f"Articles excluded due to missing dates/scores: "
          f"{len(data) - daily['article_count'].sum()}")
    print(f"Daily rows: {len(daily)}")
    print(f"Saved to: {OUTPUT_PATH.relative_to(ROOT)}")
    print("\nDaily features:")
    print(daily.to_string(index=False))


if __name__ == "__main__":
    main()
