from datetime import date, timedelta


def split_date_range(
    date_from: str,
    date_to: str,
    chunk_days: int = 30,
) -> list[tuple[str, str]]:
    """Split an inclusive date range into non-overlapping chunks."""

    start = date.fromisoformat(date_from)
    end = date.fromisoformat(date_to)

    if end < start:
        raise ValueError("date_to must not be earlier than date_from.")

    if chunk_days < 1 or chunk_days > 30:
        raise ValueError("chunk_days must be between 1 and 30.")

    ranges = []
    current = start

    while current <= end:
        chunk_end = min(current + timedelta(days=chunk_days - 1), end)
        ranges.append((current.isoformat(), chunk_end.isoformat()))
        current = chunk_end + timedelta(days=1)

    return ranges
