from unittest.mock import call

from src.ingestion import historical_calendar


def test_fetches_each_chunk_without_calling_real_api(monkeypatch):
    calls = []

    def fake_fetch_macro_calendar(**kwargs):
        calls.append(kwargs)
        return [{"eventName": f"Event {len(calls)}"}]

    monkeypatch.setattr(
        historical_calendar,
        "fetch_macro_calendar",
        fake_fetch_macro_calendar,
    )

    records = historical_calendar.fetch_historical_macro_calendar(
        actor_id="test-actor",
        date_from="2026-04-16",
        date_to="2026-06-14",
        countries=["United States"],
        impact_min="Medium",
        max_results=10,
    )

    assert len(calls) == 2
    assert calls[0]["date_from"] == "2026-04-16"
    assert calls[0]["date_to"] == "2026-05-15"
    assert calls[1]["date_from"] == "2026-05-16"
    assert calls[1]["date_to"] == "2026-06-14"
    assert all(item["actor_id"] == "test-actor" for item in calls)
    assert len(records) == 2


def test_empty_chunks_return_empty_records(monkeypatch):
    monkeypatch.setattr(
        historical_calendar,
        "fetch_macro_calendar",
        lambda **kwargs: [],
    )

    records = historical_calendar.fetch_historical_macro_calendar(
        actor_id="test-actor",
        date_from="2026-04-16",
        date_to="2026-04-16",
    )

    assert records == []