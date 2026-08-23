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

def macd(
    prices: pd.Series,
    short_period: int = 12,
    long_period: int = 26,
    signal_period: int = 9
) -> tuple[pd.Series, pd.Series]:
    if short_period <= 0 or long_period <= 0 or signal_period <= 0:
        raise ValueError("Periods must be positive.")

    if short_period >= long_period:
        raise ValueError(
            "Short period must be smaller than long period."
        )

    short_ema = ema(prices, short_period)
    long_ema = ema(prices, long_period)

    macd_line = short_ema - long_ema
    signal_line = ema(macd_line, signal_period)

    return macd_line, signal_line