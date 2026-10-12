"""Fetch recent macroeconomic news using the Exa Search API."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

EXA_URL = "https://api.exa.ai/search"


def fetch_exa_news(
    query: str = (
        "US inflation Federal Reserve interest rates "
        "employment economic outlook"
    ),
    max_results: int = 5,
) -> list[dict]:
    """Fetch a limited batch of macroeconomic news from Exa."""

    api_key = os.getenv("EXA_API_KEY")

    if not api_key or api_key == "your_exa_api_key_here":
        raise ValueError("Configure EXA_API_KEY in your .env file.")

    if not 1 <= max_results <= 5:
        raise ValueError("For the initial test, max_results must be 1–5.")

    response = requests.post(
        EXA_URL,
        headers={
            "x-api-key": api_key,
            "Content-Type": "application/json",
        },
        json={
            "query": query,
            "type": "auto",
            "category": "news",
            "numResults": max_results,
            "contents": {
                "highlights": {"maxCharacters": 500},
            },
        },
        timeout=45,
    )
    response.raise_for_status()

    payload = response.json()
    results = payload.get("results", [])

    if not isinstance(results, list):
        raise ValueError("Exa returned an unexpected response format.")

    articles = []
    for result in results:
        highlights = result.get("highlights") or []
        articles.append({
            "title": result.get("title"),
            "url": result.get("url"),
            "content": " ".join(highlights) if isinstance(highlights, list) else str(highlights),
            "published_date": result.get("publishedDate"),
            "score": result.get("score"),
            "source": "Exa",
        })

    return articles
