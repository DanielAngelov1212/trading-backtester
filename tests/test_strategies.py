import pandas as pd

from backtester.strategies import BuyAndHoldStrategy


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