# Macro Economic Outlook

**Project:** CrowdWisdomTrading Macro Economics Agent
**Report date:** 12 October 2026
**Status:** Preliminary research — not a trading recommendation

## 1. Executive Summary

The project combines historical SPY prices, FRED macroeconomic series, a preliminary economic-calendar sample, and news retrieved through Tavily and Exa. The pipeline demonstrates data processing, sentiment analysis, strategy evaluation, and chronological validation.

The current data remains insufficient to establish a reliable macro-driven trading signal. The economic-calendar sample contains only 10 events from 7 October 2026, rather than the required 180-day coverage. The combined news sample contains 10 articles, and only five have usable publication dates.

## 2. Observed Economic Signals

- **Trade Balance:** Actual value was approximately -105.6 billion versus a forecast of -100.8 billion, a difference of -4.8 billion in the source units.
- **Economic Optimism:** Actual value was 46.8 versus a forecast of 44.5, a difference of +2.3 points.
- **Atlanta Fed GDPNow:** The reported actual and forecast values were both 3.7 in this sample.
- **Other events:** Several events have missing actual or forecast values. Missing values are treated as unavailable, not as zero.

These indicators measure different economic concepts and use different units. They should not be combined into one bullish or bearish signal without a documented normalization method and additional evidence.

## 3. News Sentiment

The combined test sample contains 10 articles: five retrieved through Tavily and five through Exa. Five articles have usable publication dates, while five have missing publication dates.

The exploratory keyword-based labels are:
- Negative: 6 articles
- Neutral: 4 articles
- Positive: 0 articles

These labels are approximate and depend on the keywords used. The sample is small and is not comprehensive historical news coverage. The five dated articles are insufficient to establish a reliable sentiment trend. News sentiment is not currently used as an input to the ML strategy-permutation model.

## 4. Strategy and Model Evaluation

The baseline 20-day/50-day moving-average strategy produced a historical total return of 24.14%, compared with 38.26% for buy-and-hold. Its Sharpe ratio was 1.14, Sortino ratio was 1.64, and maximum drawdown was -8.68%.

Across five chronological test folds, the fixed moving-average strategy had mean fold total return of 4.340%, mean Sharpe ratio of 1.204, mean Sortino ratio of 1.883, and mean maximum drawdown of -4.664%. These are descriptive averages of fold metrics, not a single compounded return series.

The strategy-permutation model uses market-derived features only. Its holdout mean absolute error (MAE) was 0.005124 and root mean squared error (RMSE) was 0.007019 in daily-return units. Macro-event and news features have not yet been integrated into this model. Prediction errors do not establish trading profitability.

## 5. Data and Model Limitations

- The calendar sample does not meet the required 180-day coverage.
- FRED observation dates are not necessarily the dates when data became public; release-time alignment requires separate verification.
- Actual economic values must not enter features before their public release.
- Missing forecasts limit economic-surprise calculations.
- Five of the ten combined news articles lack usable publication dates.
- Keyword-based sentiment is exploratory and has not been validated against a labelled dataset.
- Macro and news features are not yet inputs to the ML strategy-permutation model.
- Backtests exclude transaction costs, slippage, taxes, and market impact.
- Historical performance and model predictions do not guarantee future results.

## 6. Next Steps

1. Build and validate the economic-calendar dataset over the required 180-day period.
2. Verify event publication timestamps and align event data with market data without look-ahead leakage.
3. Improve historical news coverage and evaluate sentiment against a labelled sample.
4. Integrate appropriately time-aligned macro and news features into the model.
5. Compare strategy configurations with chronological walk-forward validation.
6. Report Sharpe ratio, Sortino ratio, maximum drawdown, and benchmark comparisons on genuinely out-of-sample results.

## Conclusion

The project demonstrates a working preliminary data-processing and strategy-evaluation pipeline. However, calendar coverage, historical news coverage, and macro/news model integration remain incomplete. The current results should be treated as exploratory research, not as evidence of a validated macro-driven trading strategy.
