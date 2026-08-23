import pandas as pd


def sma(prices: pd.Series, period: int) -> pd.Series:
    if period <= 0:
        raise ValueError("Period must be positive.")

    return prices.rolling(window=period).mean()

def ema(prices: pd.Series, period: int) -> pd.Series:
    if period <= 0:
        raise ValueError("Period must be positive.")

    return prices.ewm(span=period, adjust=False).mean()