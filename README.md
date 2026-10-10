# CrowdWisdomTrading Macro Economics Agent

## Project Overview
A Python-based machine learning pipeline that combines historical trading logs, macroeconomic events, and relevant economic news to evaluate trading strategy configurations.

## Objectives
- Collect macroeconomic calendar events using Apify.
- Retrieve relevant economic news using Tavily and, if required, Exa.
- Engineer time-based and macroeconomic features.
- Predict strategy-level expected P&L or win rate.
- Evaluate models using walk-forward validation.
- Calculate Sharpe ratio, Sortino ratio, and maximum drawdown.
- Visualize macroeconomic sentiment and strategy performance.

## Technology Stack
- Python
- pandas and NumPy
- scikit-learn
- Apify
- Tavily
- SQLite
- Matplotlib
- pytest

## Project Status
Initial project setup in progress.

## Data and Reproducibility
Real trading data has not yet been connected. Synthetic data, if used during development, will be clearly identified. API keys must be stored locally in environment variables and must never be committed to version control.

## Disclaimer
This project is for research and educational purposes. Model outputs are not guarantees of future trading performance.
