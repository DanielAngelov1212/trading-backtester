import pandas as pd
import pytest

from backtester.indicators import sma, ema, rsi


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