"""Combine Tavily and Exa macro news into one dataset."""

import sys
from pathlib import Path

import pandas as pd

from src.ingestion.macro_news import fetch_macro_news
from src.ingestion.exa_macro_news import fetch_exa_news
from src.features.clean_macro_news import clean_macro_news

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT / "data" / "raw" / "macro_news_combined.csv"


def main():
    tavily_articles = fetch_macro_news(max_results=5)
    print(f"Tavily articles received: {len(tavily_articles)}")

    exa_articles = fetch_exa_news(max_results=5)
    print(f"Exa articles received: {len(exa_articles)}")

    combined = pd.DataFrame(tavily_articles + exa_articles)

    if combined.empty:
        raise ValueError("Both news providers returned no articles.")

    cleaned = clean_macro_news(combined)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_PATH, index=False)

    print(f"Combined articles before cleaning: {len(combined)}")
    print(f"Articles after cleaning/deduplication: {len(cleaned)}")
    print(f"Duplicate or unusable articles removed: {len(combined) - len(cleaned)}")
    print("Articles by source:")
    print(cleaned["source"].value_counts().to_string())
    print("Missing publication dates:", cleaned["published_date"].isna().sum())
    print(f"Saved to: {OUTPUT_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Combined news run failed: {type(exc).__name__}: {exc}")
        sys.exit(1)
