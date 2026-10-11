

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]

CALENDAR_FILE = ROOT / "data" / "processed" / "macro_features.csv"
NEWS_FILE = ROOT / "data" / "processed" / "macro_news_sentiment.csv"
REPORT_FILE = ROOT / "reports" / "macro_data_readiness.txt"


def main() -> None:
    calendar = pd.read_csv(CALENDAR_FILE)
    news = pd.read_csv(NEWS_FILE)

    calendar_dates = pd.to_datetime(
        calendar["eventDate"], errors="coerce"
    )
    news_dates = pd.to_datetime(
        news["published_date"], errors="coerce", utc=True
    )

    actual_forecast = calendar[
        ["actualValue", "forecastValue"]
    ].apply(pd.to_numeric, errors="coerce")

    usable_surprises = actual_forecast.notna().all(axis=1).sum()

    lines = [
        "MACRO DATA READINESS REPORT",
        "",
        "CALENDAR",
        f"Total events: {len(calendar)}",
        f"Valid event dates: {calendar_dates.notna().sum()}",
        f"Unique event dates: {calendar_dates.nunique()}",
        f"Events with actual and forecast: {usable_surprises}",
        f"Unique event names: {calendar['eventName'].nunique()}",
        f"High-impact events: "
        f"{calendar['is_high_impact'].fillna(0).astype(int).sum()}",
        "",
        "NEWS",
        f"Total articles: {len(news)}",
        f"Unique article URLs: {news['url'].nunique()}",
        f"Valid publication timestamps: {news_dates.notna().sum()}",
        f"Unique sentiment labels: "
        f"{news['sentiment_label'].nunique()}",
        "",
        "ASSESSMENT",
    ]

    if len(calendar) < 100 or calendar_dates.nunique() < 30:
        lines.append(
            "Calendar coverage is too small for meaningful strategy evaluation."
        )
    else:
        lines.append(
            "Calendar coverage may be sufficient for further quality checks."
        )

    if len(news) < 30:
        lines.append(
            "News sample is small; sentiment findings should be treated as exploratory."
        )
    else:
        lines.append(
            "News sample is larger, but sentiment quality still requires validation."
        )

    if usable_surprises == 0:
        lines.append(
            "No usable actual-versus-forecast observations were found."
        )
    else:
        lines.append(
            "Actual-versus-forecast observations are available for inspection."
        )

    lines.extend([
        "",
        "IMPORTANT",
        "- Event dates are not necessarily the exact public-release timestamps.",
        "- Do not use actual values before their release time.",
        "- Keyword sentiment is a baseline, not a validated market predictor.",
        "- These sample datasets do not establish trading profitability.",
    ])

    report = "\n".join(lines)
    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")

    print(report)
    print(f"\nReport saved to: {REPORT_FILE}")


if __name__ == "__main__":
    main()
