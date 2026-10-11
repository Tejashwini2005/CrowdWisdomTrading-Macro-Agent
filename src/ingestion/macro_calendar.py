
"""Fetch economic calendar events using an Apify actor."""

import os
from datetime import date, timedelta

import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_API_URL = "https://api.apify.com/v2"


def fetch_macro_calendar(
    actor_id: str,
    date_from: str,
    date_to: str,
    countries: list[str] | None = None,
    impact_min: str = "Medium",
    max_results: int = 10,
) -> list[dict]:
    """Run an Apify economic calendar actor for a date range."""

    token = os.getenv("APIFY_API_TOKEN")

    if not token or token == "your_apify_token_here":
        raise ValueError("Configure APIFY_API_TOKEN in .env.")

    if not actor_id:
        raise ValueError("Provide the Apify actor ID.")

    start = date.fromisoformat(date_from)
    end = date.fromisoformat(date_to)

    if end < start:
        raise ValueError("date_to must not be earlier than date_from.")

    if (end - start).days >= 31:
        raise ValueError("Each actor run must cover at most 31 calendar days.")

    if impact_min not in {"Low", "Medium", "High"}:
        raise ValueError("impact_min must be Low, Medium, or High.")

    if not 1 <= max_results <= 10:
        raise ValueError("For the free-plan test, max_results must be 1–10.")

    run_input = {
        "dateFrom": date_from,
        "dateTo": date_to,
        "impactMin": impact_min,
        "maxResults": max_results,
    }

    if countries:
        run_input["countries"] = countries

    response = requests.post(
        f"{APIFY_API_URL}/acts/{actor_id.replace('/', '~')}/run-sync-get-dataset-items",
        params={"token": token, "format": "json"},
        json=run_input,
        timeout=120,
    )
    response.raise_for_status()

    records = response.json()

    if not isinstance(records, list):
        raise ValueError("Apify returned an unexpected response format.")

    if any(record.get("error") for record in records if isinstance(record, dict)):
        raise RuntimeError("The Apify actor reported an error. Check its run details.")

    return records
