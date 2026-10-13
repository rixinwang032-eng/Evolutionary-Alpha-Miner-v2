"""Synthetic data used by the public demo.

The expressions are intentionally fake and are safe to publish. Replace this
module with a project-specific data adapter for real research experiments.
"""

from typing import Final

SEED_POOL: Final[tuple[tuple[str, str], ...]] = (
    ("price", "rank(ts_delta(close, 5))"),
    ("price", "rank(close / open - 1)"),
    ("price", "ts_rank(returns, 20)"),
    ("price", "rank(vwap - close)"),
    ("price", "ts_zscore(close / ts_mean(close, 20), 20)"),
    ("volume", "rank(volume / ts_mean(volume, 20))"),
    ("volume", "ts_rank(volume, 10)"),
    ("volume", "rank(adv20 / volume)"),
    ("volume", "ts_zscore(volume, 30)"),
    ("option", "rank(implied_volatility_call_120 - implied_volatility_put_120)"),
    ("option", "ts_rank(implied_volatility_call_120, 20)"),
    ("option", "rank(implied_volatility_put_120 / implied_volatility_call_120)"),
    ("fundamental", "rank(cashflow / assets)"),
    ("fundamental", "rank(sales / assets)"),
    ("fundamental", "rank(income / liabilities)"),
    ("analyst", "rank(analyst_estimate_revision)"),
    ("analyst", "ts_rank(analyst_recommendation_change, 60)"),
    ("news", "rank(news_sentiment_score)"),
    ("news", "ts_mean(news_buzz, 10)"),
    ("unknown", "rank(custom_dataset_signal)"),
)

TAG_PAIR_TARGETS: Final[tuple[tuple[str, str], ...]] = (
    ("price", "volume"),
    ("volume", "price"),
    ("price", "option"),
    ("option", "price"),
    ("price", "fundamental"),
    ("fundamental", "price"),
    ("volume", "option"),
    ("option", "volume"),
    ("volume", "fundamental"),
    ("fundamental", "volume"),
    ("news", "price"),
    ("analyst", "price"),
    ("unknown", "price"),
)
