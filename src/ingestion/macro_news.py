
"""Fetch recent macroeconomic news using the Tavily Search API."""

import os

import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_URL = "https://api.tavily.com/search"


def fetch_macro_news(
    query: str = (
        "US inflation Federal Reserve interest rates "
        "employment economic outlook"
    ),
    max_results: int = 5,
) -> list[dict]:
    """Fetch a small batch of relevant news articles."""

    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key or api_key == "your_tavily_api_key_here":
        raise ValueError("Configure TAVILY_API_KEY in your .env file.")

    if not 1 <= max_results <= 5:
        raise ValueError("For the initial test, max_results must be 1–5.")

    response = requests.post(
        TAVILY_URL,
        json={
            "api_key": api_key,
            "query": query,
            "topic": "news",
            "search_depth": "basic",
            "max_results": max_results,
            "include_answer": False,
        },
        timeout=45,
    )
    response.raise_for_status()

    payload = response.json()
    results = payload.get("results", [])

    if not isinstance(results, list):
        raise ValueError("Tavily returned an unexpected results format.")

    articles = []

    for result in results:
        articles.append({
            "title": result.get("title"),
            "url": result.get("url"),
            "content": result.get("content"),
            "published_date": result.get("published_date"),
            "score": result.get("score"),
            "source": "Tavily",
        })

    return articles
