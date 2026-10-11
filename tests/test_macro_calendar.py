
import pytest

from src.ingestion.macro_calendar import fetch_macro_calendar


def test_rejects_missing_actor_id():
    with pytest.raises(ValueError, match="Apify actor ID"):
        fetch_macro_calendar(
            actor_id="",
            date_from="2026-09-01",
            date_to="2026-09-02",
        )


def test_rejects_invalid_date_range():
    with pytest.raises(ValueError, match="earlier"):
        fetch_macro_calendar(
            actor_id="test-actor",
            date_from="2026-09-10",
            date_to="2026-09-01",
        )


def test_rejects_range_over_31_days():
    with pytest.raises(ValueError, match="at most 31"):
        fetch_macro_calendar(
            actor_id="test-actor",
            date_from="2026-08-01",
            date_to="2026-09-01",
        )


def test_rejects_invalid_impact_level():
    with pytest.raises(ValueError, match="impact_min"):
        fetch_macro_calendar(
            actor_id="test-actor",
            date_from="2026-09-01",
            date_to="2026-09-02",
            impact_min="Extreme",
        )
