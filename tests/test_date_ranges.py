import pytest

from src.ingestion.date_ranges import split_date_range


def test_splits_range_without_overlaps():
    result = split_date_range("2026-01-01", "2026-02-05")
    assert result[0] == ("2026-01-01", "2026-01-30")
    assert result[1] == ("2026-01-31", "2026-02-05")
    assert len(result) == 2


def test_single_day_range():
    assert split_date_range("2026-01-01", "2026-01-01") == [
        ("2026-01-01", "2026-01-01")
    ]


def test_rejects_reversed_dates():
    with pytest.raises(ValueError, match="earlier"):
        split_date_range("2026-02-01", "2026-01-01")


@pytest.mark.parametrize("chunk_days", [0, -1, 31])
def test_rejects_invalid_chunk_size(chunk_days):
    with pytest.raises(ValueError, match="between 1 and 30"):
        split_date_range("2026-01-01", "2026-02-01", chunk_days)
