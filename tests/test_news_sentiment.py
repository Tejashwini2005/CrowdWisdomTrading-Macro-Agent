
import pandas as pd

from src.features.news_sentiment import score_news_sentiment


def test_positive_news_is_labelled_positive():
    data = pd.DataFrame({
        "title": ["Strong economic growth"],
        "content": ["The recovery continues to improve."],
    })

    result = score_news_sentiment(data)

    assert result.loc[0, "sentiment_label"] == "positive"
    assert result.loc[0, "sentiment_score"] > 0


def test_negative_news_is_labelled_negative():
    data = pd.DataFrame({
        "title": ["Inflation risk and recession"],
        "content": ["Economic uncertainty remains high."],
    })

    result = score_news_sentiment(data)

    assert result.loc[0, "sentiment_label"] == "negative"
    assert result.loc[0, "sentiment_score"] < 0


def test_neutral_news_is_labelled_neutral():
    data = pd.DataFrame({
        "title": ["Federal Reserve meeting scheduled"],
        "content": ["Officials will meet next Wednesday."],
    })

    result = score_news_sentiment(data)

    assert result.loc[0, "sentiment_label"] == "neutral"
    assert result.loc[0, "sentiment_score"] == 0
