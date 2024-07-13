from typing import Literal
import yfinance
from cachetools import cached, TTLCache
import pandas as pd
from all_weather.utils import to_snake_case

Period = Literal["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]


@cached(cache=TTLCache(maxsize=10, ttl=60))
def get_price(symbol: str) -> float:
    """Gets the price of an equity from the Yahoo Finance API."""
    ticker = yfinance.Ticker(symbol)
    bid = ticker.info["bid"]
    ask = ticker.info["ask"]
    price = (bid + ask) / 2
    return price


def get_historical_data(symbol: str, period: Period = "10y") -> pd.Series:
    ticker = yfinance.Ticker(symbol)
    data = ticker.history(period=period)
    data.index.name = to_snake_case(data.index.name)
    data.columns = [to_snake_case(column) for column in data.columns]
    prices = data["close"]
    return prices


def get_multiple_historical_data(symbols: list[str], period: Period = "10y") -> pd.DataFrame:
    data = {}
    for symbol in symbols:
        prices = get_historical_data(symbol, period)
        data[symbol] = prices
    prices = pd.DataFrame(data)
    prices = prices.round(2)
    prices = prices.dropna()
    return prices
