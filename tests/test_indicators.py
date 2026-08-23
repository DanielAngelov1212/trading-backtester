import pandas as pd
import pytest

from backtester.indicators import sma, ema, rsi, macd


def test_sma():
    prices = pd.Series([10, 20, 30, 40, 50])

    result = sma(prices, 3)

    assert result.iloc[2] == 20
    assert result.iloc[3] == 30
    assert result.iloc[4] == 40


def test_sma_invalid_period():
    prices = pd.Series([10, 20, 30])

    with pytest.raises(ValueError):
        sma(prices, 0)

def test_ema():
    prices = pd.Series([10, 20, 30, 40, 50])

    result = ema(prices, 3)

    assert len(result) == 5
    assert result.iloc[-1] > result.iloc[0]


def test_ema_invalid_period():
    prices = pd.Series([10, 20, 30])

    with pytest.raises(ValueError):
        ema(prices, 0)

def test_rsi():
    prices = pd.Series([
        10, 11, 12, 11, 13,
        14, 15, 14, 16, 17
    ])

    result = rsi(prices, period=3)

    valid_values = result.dropna()

    assert not valid_values.empty
    assert valid_values.between(0, 100).all()


def test_rsi_invalid_period():
    prices = pd.Series([10, 20, 30])

    with pytest.raises(ValueError):
        rsi(prices, 0)

def test_macd():
    prices = pd.Series([
        10, 11, 12, 13, 14,
        15, 16, 17, 18, 19
    ])

    macd_line, signal_line = macd(
        prices,
        short_period=3,
        long_period=5,
        signal_period=2
    )

    assert len(macd_line) == len(prices)
    assert len(signal_line) == len(prices)


def test_macd_invalid_period():
    prices = pd.Series([10, 20, 30])

    with pytest.raises(ValueError):
        macd(
            prices,
            short_period=0,
            long_period=5
        )


def test_macd_short_period_greater_than_long():
    prices = pd.Series([10, 20, 30])

    with pytest.raises(ValueError):
        macd(
            prices,
            short_period=10,
            long_period=5
        )