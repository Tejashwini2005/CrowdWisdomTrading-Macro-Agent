
import pandas as pd

from src.features.clean_macro_news import clean_macro_news


def test_news_cleaning_removes_duplicate_urls():
    data = pd.DataFrame({
        "title": ["Fed outlook", "Fed outlook duplicate"],
        "url": [
            "https://example.com/fed",
            "https://example.com/fed",
        ],
        "content": ["First article", "Duplicate article"],
        "published_date": [
            "Wed, 16 Sep 2026 19:45:37 GMT",
            "Wed, 16 Sep 2026 19:45:37 GMT",
        ],
    })

    cleaned = clean_macro_news(data)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["title"] == "Fed outlook"


def test_news_cleaning_parses_dates_as_utc():
    data = pd.DataFrame({
        "title": ["Inflation outlook"],
        "url": ["https://example.com/inflation"],
        "published_date": ["Wed, 16 Sep 2026 19:45:37 GMT"],
    })

    cleaned = clean_macro_news(data)

    assert str(cleaned.loc[0, "published_date"].tz) == "UTC"


def test_news_cleaning_removes_missing_titles():
    data = pd.DataFrame({
        "title": ["Useful article", None, "   "],
        "url": [
            "https://example.com/1",
            "https://example.com/2",
            "https://example.com/3",
        ],
    })

    cleaned = clean_macro_news(data)

    assert len(cleaned) == 1
    assert cleaned.iloc[0]["title"] == "Useful article"
