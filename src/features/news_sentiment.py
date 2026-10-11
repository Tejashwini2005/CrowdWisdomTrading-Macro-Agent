
"""Estimate news sentiment using a simple keyword baseline."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "processed" / "macro_news_clean.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "macro_news_sentiment.csv"

POSITIVE_TERMS = {
    "growth", "improve", "improved", "strong", "stronger",
    "optimistic", "ease", "easing", "cooling", "recovery",
    "beat", "beats", "decline", "lower",
}

NEGATIVE_TERMS = {
    "inflation", "uncertainty", "uncertain", "hike", "hikes",
    "tightening", "recession", "weak", "weaker", "risk",
    "risks", "crisis", "surge", "surging", "higher",
}


def score_news_sentiment(data: pd.DataFrame) -> pd.DataFrame:
    """Add keyword scores and approximate sentiment labels."""
    scored = data.copy()

    if "title" not in scored.columns:
        raise ValueError("News data must contain a title column.")

    text = scored["title"].fillna("").astype(str).str.lower()

    if "content" in scored.columns:
        text = text + " " + scored["content"].fillna("").astype(str).str.lower()

    def score_text(article_text: str) -> int:
        words = set(article_text.split())
        positive_count = len(words & POSITIVE_TERMS)
        negative_count = len(words & NEGATIVE_TERMS)
        return positive_count - negative_count

    scored["sentiment_score"] = text.map(score_text)

    scored["sentiment_label"] = scored["sentiment_score"].map(
        lambda score: (
            "positive" if score > 0
            else "negative" if score < 0
            else "neutral"
        )
    )

    scored["sentiment_method"] = "keyword_baseline"
    return scored


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"Clean news file not found: {INPUT_PATH}"
        )

    news = pd.read_csv(INPUT_PATH)
    scored = score_news_sentiment(news)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    scored.to_csv(OUTPUT_PATH, index=False)

    print(f"Articles scored: {len(scored)}")
    print(f"Saved to: {OUTPUT_PATH.relative_to(ROOT)}")
    print("Sentiment counts:")
    print(scored["sentiment_label"].value_counts().to_string())
    print("\nArticle preview:")
    print(
        scored[["title", "sentiment_score", "sentiment_label"]]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
