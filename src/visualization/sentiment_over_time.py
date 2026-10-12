
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "processed" / "macro_news_sentiment.csv"
OUTPUT_DIR = ROOT / "reports" / "figures"
OUTPUT_PATH = OUTPUT_DIR / "macro_sentiment_over_time.png"


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Sentiment data not found: {INPUT_PATH}")

    data = pd.read_csv(INPUT_PATH)

    required = {"published_date", "sentiment_score", "title"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    data["published_date"] = pd.to_datetime(
        data["published_date"], utc=True, errors="coerce"
    )
    data["sentiment_score"] = pd.to_numeric(
        data["sentiment_score"], errors="coerce"
    )
    data = data.dropna(subset=["published_date", "sentiment_score"])
    data = data.sort_values("published_date")

    if data.empty:
        raise ValueError("No valid dated sentiment observations are available.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        data["published_date"],
        data["sentiment_score"],
        marker="o",
        linewidth=1.5,
    )
    ax.axhline(0, linestyle="--", linewidth=1)
    ax.set_title("Macro News Sentiment Over Time")
    ax.set_xlabel("Publication date (UTC)")
    ax.set_ylabel("Keyword-based sentiment score")
    ax.grid(True, alpha=0.3)
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=160)
    plt.close(fig)

    print(f"Valid dated articles: {len(data)}")
    print(f"Date range: {data['published_date'].min()} to {data['published_date'].max()}")
    print(f"Sentiment labels: {data['sentiment_label'].value_counts().to_dict()}")
    print(f"Chart saved to: {OUTPUT_PATH.relative_to(ROOT)}")
    print("Caution: sparse keyword-based observations; not a validated market signal.")


if __name__ == "__main__":
    main()
