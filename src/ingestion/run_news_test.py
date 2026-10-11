
"""Run a limited macroeconomic news test and save the results."""

import sys
from pathlib import Path

import pandas as pd

from src.ingestion.macro_news import fetch_macro_news


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_PATH = ROOT / "data" / "raw" / "macro_news_test.csv"


def main():
    articles = fetch_macro_news(max_results=5)

    if not articles:
        print("Tavily returned no articles for this query.")
        return

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(articles).to_csv(OUTPUT_PATH, index=False)

    print(f"Articles received: {len(articles)}")
    print(f"Saved results to: {OUTPUT_PATH.relative_to(ROOT)}")
    print("Available fields:", ", ".join(articles[0].keys()))

    for article in articles:
        print(f"- {article.get('title', 'Untitled')}")
        print(f"  Published: {article.get('published_date') or 'Date not provided'}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"News test failed: {type(exc).__name__}: {exc}")
        sys.exit(1)
