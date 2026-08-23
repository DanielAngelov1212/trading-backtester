import pandas as pd


def sma(prices: pd.Series, period: int) -> pd.Series:
    if period <= 0:
        raise ValueError("Period must be positive.")

    return prices.rolling(window=period).mean()

def ema(prices: pd.Series, period: int) -> pd.Series:
    if period <= 0:
        raise ValueError("Period must be positive.")

    return prices.ewm(span=period, adjust=False).mean()

def rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    if period <= 0:
        raise ValueError("Period must be positive.")

    delta = prices.diff()

    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)

    average_gain = gains.rolling(window=period).mean()
    average_loss = losses.rolling(window=period).mean()

    rs = average_gain / average_loss

    return 100 - (100 / (1 + rs))