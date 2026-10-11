 CrowdWisdomTrading Macro Economics Agent

 Project Overview

A Python-based research pipeline for collecting US macroeconomic indicators, economic calendar events, financial news, and historical market data. The project engineers features, explores news sentiment, and evaluates a baseline moving-average strategy against a buy-and-hold benchmark.

 Objectives

- Collect economic calendar events and macroeconomic observations.
- Retrieve economic news and perform exploratory keyword-based sentiment analysis.
- Download and validate historical market data.
- Engineer time-based and macroeconomic features.
- Evaluate a baseline trading strategy using historical and chronological holdout data.
- Report returns, volatility, Sharpe ratio, Sortino ratio, and maximum drawdown.
- Generate sentiment visualizations and data-quality reports.

 Technology Stack

- Python
- pandas and NumPy
- yfinance
- FRED API
- Apify
- Tavily and Exa
- Matplotlib
- pytest
- Requests and python-dotenv

 Implemented Components

- Market data ingestion and validation.
- Economic calendar ingestion and feature engineering.
- FRED historical macroeconomic data ingestion.
- Economic news processing and keyword-based sentiment scoring.
- A 20-day/50-day moving-average baseline strategy.
- Baseline and chronological holdout evaluations.
- Macro data readiness and FRED data-quality reports.
- Sentiment visualizations and automated tests.

 Current Data Coverage

- SPY: 501 daily observations, 10 October 2024 to 9 October 2026.
- FRED: 23 observations across unemployment, CPI, federal funds rate, and nonfarm payrolls.
- Economic calendar sample: 10 events across one unique event date.
- News sample: 5 articles with 5 unique URLs.

The macro calendar and news samples are small and are not sufficient to establish the predictive value of macroeconomic signals or news sentiment.

## Evaluation Results

 Full Historical Period

| Metric | Moving-Average Strategy | Buy and Hold |
|---|---:|---:|
| Total return | 24.14% | 38.26% |
| Annualized return | 11.49% | 17.70% |
| Annualized volatility | 9.96% | 16.51% |
| Sharpe ratio | 1.14 | 1.07 |
| Sortino ratio | 1.64 | 1.60 |
| Maximum drawdown | -8.68% | -18.76% |

 Chronological Holdout Period

| Metric | Moving-Average Strategy | Buy and Hold |
|---|---:|---:|
| Total return | 10.45% | 15.17% |
| Annualized return | 18.05% | 26.58% |
| Annualized volatility | 10.63% | 13.40% |
| Sharpe ratio | 1.61 | 1.83 |
| Sortino ratio | 2.50 | 2.87 |
| Maximum drawdown | -4.49% | -6.57% |

The strategy had lower volatility and smaller maximum drawdowns in these evaluations, but it underperformed buy and hold on total return in both periods. Holdout results come from one chronological split, not rolling walk-forward validation.

Transaction costs, slippage, and taxes are excluded. A zero risk-free rate is assumed in the reported Sharpe and Sortino calculations.

 * Validation and Reports

The project includes automated tests and scripts for market-data validation, FRED data-quality validation, macro readiness assessment, baseline evaluation, and chronological holdout evaluation.

Reports are stored in `reports/`, and sentiment charts are stored in `reports/figures/`.

Run the automated tests with:

```powershell
python -m pytest -q
```

 * Setup

1. Create and activate a Python virtual environment.
2. Install the packages listed in `requirements.txt`, if that file is provided and current.
3. Configure required API keys locally in `.env`.
4. Run the ingestion and validation modules from the project root.

Example commands:

```powershell
python -m src.ingestion.fred_macro_data
python -m src.validation.validate_fred_data
python -m src.validation.validate_market_data
python -m src.validation.check_macro_readiness
python -m pytest -q
```

Do not commit `.env` or expose API keys. Keep `.env.example` limited to placeholder values.

 Limitations and Future Work

- Expand economic calendar coverage across a meaningful historical period.
- Increase the news sample and evaluate sentiment labels more carefully.
- Add point-in-time macro data and reliable public-release timestamps.
- Obtain and validate consensus forecasts before studying event surprises.
- Implement repeated chronological walk-forward validation.
- Include realistic transaction costs and slippage.
- Evaluate whether macroeconomic features improve performance beyond a simple baseline.

FRED observation dates are not necessarily public-release dates, and historical values may be revised. The current data do not establish that macroeconomic signals improve trading results.

 Disclaimer

This project is for research and educational purposes only. Historical performance does not guarantee future results, and this project does not establish a profitable trading system.
