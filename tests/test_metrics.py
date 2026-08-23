import pandas as pd

from backtester.metrics import (
    max_drawdown,
    sharpe_ratio,
    total_return,
    return_on_risked_capital,
    risked_capital,
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


def test_risked_capital():
    trades = [
        {
            "action": "BUY",
            "price": 100,
            "quantity": 8,
        },
        {
            "action": "SELL",
            "price": 120,
            "quantity": 8,
        },
        {
            "action": "BUY",
            "price": 110,
            "quantity": 9,
        },
    ]

    result = risked_capital(trades)

    assert result == 990


def test_risked_capital_no_trades():
    result = risked_capital([])

    assert result == 0


def test_return_on_risked_capital():
    result = return_on_risked_capital(
        initial_capital=1000,
        final_value=1200,
        risked_amount=800
    )

    assert result == 25


def test_return_on_risked_capital_no_risk():
    result = return_on_risked_capital(
        initial_capital=1000,
        final_value=1000,
        risked_amount=0
    )

    assert result == 0
