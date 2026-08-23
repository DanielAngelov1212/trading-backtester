import pandas as pd

from backtester.metrics import (
    max_drawdown,
    sharpe_ratio,
    total_return,
)


def test_total_return():
    result = total_return(
        initial_capital=1000,
        final_value=1200
    )

    assert result == 20


def test_negative_total_return():
    result = total_return(
        initial_capital=1000,
        final_value=800
    )

    assert result == -20


def test_max_drawdown():
    values = pd.Series([
        1000,
        1200,
        1100,
        900,
        1300
    ])

    result = max_drawdown(values)

    assert result == -25


def test_sharpe_ratio_constant_values():
    values = pd.Series([
        1000,
        1000,
        1000,
        1000
    ])

    result = sharpe_ratio(values)

    assert result == 0