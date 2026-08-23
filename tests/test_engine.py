import pandas as pd
import pytest

from backtester.engine import Backtest
from backtester.strategies import BuyAndHoldStrategy


def test_backtest_runs():
    data = pd.DataFrame(
        {
            "Close": [100, 110, 120]
        }
    )

    strategy = BuyAndHoldStrategy()

    backtest = Backtest(
        data=data,
        strategy=strategy,
        initial_capital=1000
    )

    results = backtest.run()

    assert "Signal" in results.columns
    assert "PortfolioValue" in results.columns
    assert len(results) == 3


def test_buy_and_hold_backtest():
    data = pd.DataFrame(
        {
            "Close": [100, 110, 120]
        }
    )

    strategy = BuyAndHoldStrategy()

    backtest = Backtest(
        data=data,
        strategy=strategy,
        initial_capital=1000
    )

    results = backtest.run()

    final_value = results["PortfolioValue"].iloc[-1]

    assert final_value == 1200


def test_backtest_empty_data():
    data = pd.DataFrame()

    strategy = BuyAndHoldStrategy()

    with pytest.raises(ValueError):
        Backtest(
            data=data,
            strategy=strategy,
            initial_capital=1000
        )