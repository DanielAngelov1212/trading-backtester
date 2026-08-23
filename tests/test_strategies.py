import pandas as pd
import pytest

from backtester.strategies import (
    BuyAndHoldStrategy,
    MACDStrategy,
    MovingAverageStrategy,
    RSIStrategy,
)


def test_buy_and_hold_strategy():
    data = pd.DataFrame(
        {
            "Close": [100, 105, 110]
        }
    )

    strategy = BuyAndHoldStrategy()

    signals = strategy.generate_signals(data)

    assert signals.iloc[0] == "BUY"
    assert signals.iloc[1] == "HOLD"
    assert signals.iloc[2] == "HOLD"


def test_buy_and_hold_empty_data():
    data = pd.DataFrame()

    strategy = BuyAndHoldStrategy()

    signals = strategy.generate_signals(data)

    assert signals.empty


def test_moving_average_strategy_returns_signals():
    data = pd.DataFrame(
        {
            "Close": [
                10, 10, 10, 10, 10,
                20, 30, 40, 50, 60
            ]
        }
    )

    strategy = MovingAverageStrategy(
        short_period=2,
        long_period=3
    )

    signals = strategy.generate_signals(data)

    assert len(signals) == len(data)
    assert set(signals.unique()).issubset(
        {"BUY", "SELL", "HOLD"}
    )


def test_moving_average_invalid_periods():
    with pytest.raises(ValueError):
        MovingAverageStrategy(
            short_period=10,
            long_period=5
        )


def test_moving_average_generates_buy_signal():
    data = pd.DataFrame(
        {
            "Close": [
                10, 10, 10, 10,
                10, 10, 20, 30
            ]
        }
    )

    strategy = MovingAverageStrategy(
        short_period=2,
        long_period=3
    )

    signals = strategy.generate_signals(data)

    assert "BUY" in signals.values


def test_rsi_strategy_returns_signals():
    data = pd.DataFrame(
        {
            "Close": [
                10, 9, 8, 7, 6,
                7, 8, 9, 10, 11
            ]
        }
    )

    strategy = RSIStrategy(period=3)

    signals = strategy.generate_signals(data)

    assert len(signals) == len(data)
    assert set(signals.unique()).issubset(
        {"BUY", "SELL", "HOLD"}
    )


def test_rsi_strategy_generates_buy_signal():
    data = pd.DataFrame(
        {
            "Close": [
                10, 9, 8, 7, 6, 5
            ]
        }
    )

    strategy = RSIStrategy(period=3)

    signals = strategy.generate_signals(data)

    assert "BUY" in signals.values


def test_rsi_strategy_invalid_thresholds():
    with pytest.raises(ValueError):
        RSIStrategy(
            oversold=80,
            overbought=20
        )


def test_macd_strategy_returns_signals():
    data = pd.DataFrame(
        {
            "Close": [
                10, 10, 10, 10, 10,
                11, 12, 13, 14, 15,
                14, 13, 12, 11, 10
            ]
        }
    )

    strategy = MACDStrategy(
        short_period=2,
        long_period=4,
        signal_period=2
    )

    signals = strategy.generate_signals(data)

    assert len(signals) == len(data)
    assert set(signals.unique()).issubset(
        {"BUY", "SELL", "HOLD"}
    )


def test_macd_strategy_generates_signal():
    data = pd.DataFrame(
        {
            "Close": [
                10, 10, 10, 10, 10,
                12, 14, 16, 18, 20
            ]
        }
    )

    strategy = MACDStrategy(
        short_period=2,
        long_period=4,
        signal_period=2
    )

    signals = strategy.generate_signals(data)

    assert "BUY" in signals.values


def test_macd_strategy_invalid_periods():
    with pytest.raises(ValueError):
        MACDStrategy(
            short_period=10,
            long_period=5
        )
