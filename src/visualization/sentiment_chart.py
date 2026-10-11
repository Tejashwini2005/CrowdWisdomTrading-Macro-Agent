
"""Create visualizations of the macro news sentiment results."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "processed" / "macro_news_sentiment.csv"
OUTPUT_DIR = ROOT / "reports" / "figures"


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Sentiment data not found: {INPUT_PATH}"
        )

    data = pd.read_csv(INPUT_PATH)

    required = {"title", "sentiment_label", "sentiment_score"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Chart 1: sentiment distribution.
    counts = (
        data["sentiment_label"]
        .value_counts()
        .reindex(["positive", "neutral", "negative"], fill_value=0)
    )

    fig, ax = plt.subplots(figsize=(7, 5))
    counts.plot(kind="bar", ax=ax)
    ax.set_title("Macroeconomic News Sentiment Distribution")
    ax.set_xlabel("Sentiment label")
    ax.set_ylabel("Number of articles")
    ax.tick_params(axis="x", rotation=0)
    fig.tight_layout()

    distribution_path = OUTPUT_DIR / "sentiment_distribution.png"
    fig.savefig(distribution_path, dpi=150)
    plt.close(fig)

    # Chart 2: score for each article.
    chart_data = data.copy()
    chart_data["short_title"] = chart_data["title"].str.slice(0, 55)

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.barh(chart_data["short_title"], chart_data["sentiment_score"])
    ax.set_title("Keyword-Based Sentiment Scores by Article")
    ax.set_xlabel("Sentiment score (positive minus negative keywords)")
    ax.set_ylabel("Article")
    ax.invert_yaxis()
    fig.tight_layout()

    scores_path = OUTPUT_DIR / "sentiment_scores.png"
    fig.savefig(scores_path, dpi=150)
    plt.close(fig)

    print(f"Articles visualized: {len(data)}")
    print(f"Saved: {distribution_path.relative_to(ROOT)}")
    print(f"Saved: {scores_path.relative_to(ROOT)}")
    print("Note: These are keyword-baseline labels, not market predictions.")


if __name__ == "__main__":
    main()
