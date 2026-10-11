
"""Clean and deduplicate macroeconomic news articles."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
INPUT_PATH = ROOT / "data" / "raw" / "macro_news_test.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "macro_news_clean.csv"


def clean_macro_news(data: pd.DataFrame) -> pd.DataFrame:
    """Normalize news fields and remove unusable or duplicate articles."""
    cleaned = data.copy()

    for column in ["title", "url", "content", "source"]:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].astype("string").str.strip()
            cleaned[column] = cleaned[column].replace("", pd.NA)

    if "published_date" in cleaned.columns:
        cleaned["published_date"] = pd.to_datetime(
            cleaned["published_date"],
            errors="coerce",
            utc=True,
        )

    if "score" in cleaned.columns:
        cleaned["score"] = pd.to_numeric(
            cleaned["score"], errors="coerce"
        )

    if "title" in cleaned.columns:
        cleaned = cleaned[cleaned["title"].notna()]

    if "url" in cleaned.columns:
        cleaned = cleaned.drop_duplicates(subset=["url"], keep="first")

    return cleaned.reset_index(drop=True)


def main() -> None:
    if not INPUT_PATH.exists():
        raise FileNotFoundError(
            f"News data not found: {INPUT_PATH}. Run the news test first."
        )

    raw = pd.read_csv(INPUT_PATH)
    cleaned = clean_macro_news(raw)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(OUTPUT_PATH, index=False)

    print(f"Raw articles: {len(raw)}")
    print(f"Clean articles: {len(cleaned)}")
    print(f"Removed articles: {len(raw) - len(cleaned)}")
    print(f"Saved to: {OUTPUT_PATH.relative_to(ROOT)}")

    if "published_date" in cleaned.columns:
        print("Missing publication dates:", cleaned["published_date"].isna().sum())


if __name__ == "__main__":
    main()
