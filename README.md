 CrowdWisdomTrading Macro Economics Agent

 Project Overview

A Python-based research prototype for collecting US macroeconomic data, economic calendar events, financial news, and historical market data. The project engineers features, analyzes news sentiment, and evaluates a baseline moving-average strategy and a Random Forest strategy-permutation model.

It compares historical strategy performance with a buy-and-hold benchmark using chronological holdout and expanding-window evaluation.

 Objectives

- Collect and validate historical market data and macroeconomic observations.
- Ingest economic calendar events and financial news.
- Perform exploratory keyword-based sentiment analysis.
- Engineer market and macroeconomic features.
- Evaluate a moving-average strategy against buy-and-hold.
- Explore Random Forest predictions across moving-average configurations.
- Generate visualizations, validation reports, and automated tests.

 Technology Stack

- Python
- pandas and NumPy
- scikit-learn
- yfinance
- FRED API
- Apify
- Tavily and Exa
- Matplotlib and Seaborn
- Requests and python-dotenv
- PyYAML
- pytest

 Implemented Components

- Historical market-data ingestion and validation.
- FRED macroeconomic data ingestion and quality checks.
- Economic calendar ingestion and date-range utilities.
- News ingestion, cleaning, and keyword-based sentiment scoring.
- A 20-day/50-day moving-average baseline strategy.
- Chronological holdout evaluation against buy-and-hold.
- Five-split expanding-window evaluation of the fixed baseline strategy.
- Random Forest regression for next-day strategy-return estimates across five moving-average configurations.
- Macro data readiness reporting.
- Sentiment and strategy performance visualizations.
- Automated tests for data processing and date-range utilities.

 Current Data Coverage

- **Market data:** 501 SPY daily observations from 10 October 2024 to 9 October 2026.
- **FRED data:** 23 observations across unemployment, CPI, the federal funds rate, and nonfarm payrolls.
- **Economic calendar:** 10 events across one unique event date.
- **News:** 10 combined articles, comprising 5 from Tavily and 5 from Exa. Five articles have valid publication dates; five have missing publication dates.

These datasets are limited research samples. They are not comprehensive historical coverage and do not establish that macroeconomic signals or news sentiment predict market movements.

 Evaluation Results

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

The development period contains 350 observations, and the holdout period contains 151 observations.

| Metric | Moving-Average Strategy | Buy and Hold |
|---|---:|---:|
| Total return | 10.45% | 15.17% |
| Annualized volatility | 10.63% | 13.40% |
| Sharpe ratio | 1.61 | 1.83 |
| Sortino ratio | 2.50 | 2.87 |
| Maximum drawdown | -4.49% | -6.57% |

The moving-average strategy had lower volatility and smaller maximum drawdowns in these evaluations, but lower total returns in both periods.

### Expanding-Window Evaluation

The fixed 20-day/50-day strategy was evaluated over five sequential test windows.

| Average Test-Fold Metric | Strategy | Buy and Hold |
|---|---:|---:|
| Total return per fold | 4.34% | 5.51% |
| Annualized return | 14.59% | 18.30% |
| Annualized volatility | 10.52% | 15.65% |
| Sharpe ratio | 1.204 | 1.519 |
| Sortino ratio | 1.883 | 2.323 |
| Maximum drawdown | -4.66% | -7.75% |

These are descriptive averages of fold-level metrics, not the results of one compounded portfolio. The strategy is fixed rather than retrained in each fold.

 Random Forest Strategy-Permutation Model

The model estimates next-day strategy returns for five moving-average configurations:

- 5/20 days
- 10/30 days
- 20/50 days
- 20/100 days
- 50/100 days

It uses market-derived features, including lagged returns, historical volatility, momentum, moving-average gaps, and configuration windows.

Reported chronological holdout results:

- Training rows: 1,728
- Test rows: 480
- Mean absolute error (MAE): 0.005124
- Root mean squared error (RMSE): 0.007019

The model currently does not use macroeconomic or news sentiment features for return predictions. Prediction-error metrics do not establish strategy profitability.

Transaction costs, slippage, taxes, and market impact are excluded from the reported strategy evaluations. A zero risk-free rate is assumed in the reported Sharpe and Sortino calculations.

## Reports and Visualizations

Reports are stored in `reports/`.

The project generates six figures in `reports/figures/`:

- `sentiment_distribution.png` — distribution of keyword-based sentiment labels.
- `sentiment_scores.png` — sentiment scores for collected news articles.
- `macro_sentiment_over_time.png` — sentiment observations for articles with valid publication dates.
- `holdout_equity_comparison.png` — holdout equity comparison between the strategy and buy-and-hold.
- `walk_forward_returns.png` — returns across chronological test folds.
- `configuration_holdout_returns.png` — holdout returns for tested moving-average configurations.

The charts describe the available samples and evaluation results; they do not establish future profitability.

## Run the Local Pipeline

Preview the planned stages without executing them:

```powershell
python -m src.main --dry-run
```

Run the local processing and evaluation pipeline:

```powershell
python -m src.main
```

The pipeline requires non-empty local input files: `data/raw/macro_calendar_test.csv`, `data/raw/macro_news_combined.csv`, and `data/raw/spy_historical_prices.csv`.

This entry point does not perform live API ingestion. It runs local processing, strategy evaluation, walk-forward validation, and the strategy-permutation stage. Strategy charts are generated when their required processed inputs exist.

 Setup

 1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

 3. Configure API keys

Create a local `.env` file in the project root using `.env.example` as a template. Add your own API keys locally for the integrations you intend to use.

Do not commit `.env` or expose API keys. Keep `.env.example` limited to placeholder values.

 4. Run validation and reports

Run commands from the project root. For example:

```powershell
python -m src.validation.validate_fred_data
python -m src.validation.validate_market_data
python -m src.validation.check_macro_readiness
```

Individual ingestion and evaluation modules may require API credentials or network access.

 5. Run automated tests

```powershell
python -m pytest -q
```

The project test suite passed 27 tests during the final review.

 Limitations and Future Work

- Expand economic calendar coverage across a meaningful historical period.
- Collect more news articles and validate sentiment classifications.
- Incorporate point-in-time macroeconomic data and reliable public-release timestamps.
- Obtain and validate consensus forecasts before studying event surprises.
- Evaluate realistic transaction costs, slippage, taxes, and market impact.
- Assess leakage-aware model selection and further out-of-sample performance.
- Investigate macroeconomic features only after sufficient aligned historical data are available.
- Evaluate performance across additional assets and market regimes.

FRED observation dates are not necessarily public-release dates, and historical values may be revised. The current datasets do not establish that macroeconomic signals improve trading results.

 Disclaimer

This project is for research and educational purposes only. Historical performance does not guarantee future results. The project does not establish a profitable trading system and does not provide investment advice.
