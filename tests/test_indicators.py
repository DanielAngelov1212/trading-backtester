import pandas as pd
import pytest

from backtester.indicators import sma


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