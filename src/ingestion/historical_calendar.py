"""Historical macro-calendar fetching, separated from the live test runner."""

from src.ingestion.date_ranges import split_date_range
from src.ingestion.macro_calendar import fetch_macro_calendar


def fetch_historical_macro_calendar(
    actor_id: str,
    date_from: str,
    date_to: str,
    countries: list[str] | None = None,
    impact_min: str = "Medium",
    max_results: int = 10,
) -> list[dict]:
    """Fetch each date chunk and combine the returned events.

    Calling this function makes real Apify requests. Use mocked tests
    when verifying the chunking behavior.
    """

    chunks = split_date_range(date_from, date_to)
    all_records: list[dict] = []

    for chunk_from, chunk_to in chunks:
        records = fetch_macro_calendar(
            actor_id=actor_id,
            date_from=chunk_from,
            date_to=chunk_to,
            countries=countries,
            impact_min=impact_min,
            max_results=max_results,
        )
        all_records.extend(records)

    return all_records