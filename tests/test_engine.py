import pandas as pd
import pytest

from backtester.engine import (
    Backtest,
    compare_with_buy_and_hold,
)
from backtester.strategies import BuyAndHoldStrategy
from backtester.metrics import (
    max_drawdown,
    sharpe_ratio,
    total_return,
)


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


def test_backtest_metrics():
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

    return_value = total_return(
        initial_capital=1000,
        final_value=final_value
    )

    drawdown = max_drawdown(
        results["PortfolioValue"]
    )

    sharpe = sharpe_ratio(
        results["PortfolioValue"]
    )

    assert final_value == 1200
    assert return_value == 20
    assert drawdown == 0
    assert sharpe >= 0


def test_compare_with_buy_and_hold():
    data = pd.DataFrame(
        {
            "Close": [100, 110, 120]
        }
    )

    comparison = compare_with_buy_and_hold(
        data=data,
        strategy=BuyAndHoldStrategy(),
        initial_capital=1000
    )

    assert comparison["strategy_final_value"] == 1200
    assert comparison["buy_hold_final_value"] == 1200

    assert comparison["strategy_return"] == 20
    assert comparison["buy_hold_return"] == 20
