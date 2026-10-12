"""Run a limited Exa macro-news test and save the results."""

import sys
from pathlib import Path

import pandas as pd

from src.ingestion.exa_macro_news import fetch_exa_news

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT / "data" / "raw" / "exa_macro_news_test.csv"


def main():
    articles = fetch_exa_news(max_results=5)

    if not articles:
        print("Exa returned no articles for this test.")
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(articles).to_csv(OUTPUT_PATH, index=False)

    print(f"Articles received: {len(articles)}")
    print(f"Saved results to: {OUTPUT_PATH.relative_to(ROOT)}")

    for article in articles:
        print(f"- {article.get('title') or 'Untitled'}")
        print(f"  Published: {article.get('published_date') or 'Not provided'}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Exa test failed: {type(exc).__name__}: {exc}")
        sys.exit(1)
