import yfinance
from cachetools import cached, TTLCache


@cached(cache=TTLCache(maxsize=10, ttl=60))
def get_price(symbol: str) -> float:
    """Gets the price of an equity from the Yahoo Finance API."""
    ticker = yfinance.Ticker(symbol)
    bid = ticker.info["bid"]
    ask = ticker.info["ask"]
    price = (bid + ask) / 2
    return price
