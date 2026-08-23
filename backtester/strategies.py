from abc import ABC, abstractmethod
from backtester.indicators import sma

import pandas as pd


class Strategy(ABC):

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        pass


class BuyAndHoldStrategy(Strategy):

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        signals = pd.Series("HOLD", index=data.index)

        if not data.empty:
            signals.iloc[0] = "BUY"

        return signals

class MovingAverageStrategy(Strategy):

    def __init__(
        self,
        short_period: int = 20,
        long_period: int = 50
    ) -> None:
        if short_period <= 0 or long_period <= 0:
            raise ValueError("Periods must be positive.")

        if short_period >= long_period:
            raise ValueError(
                "Short period must be smaller than long period."
            )

        self.short_period = short_period
        self.long_period = long_period

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        short_sma = sma(data["Close"], self.short_period)
        long_sma = sma(data["Close"], self.long_period)

        signals = pd.Series("HOLD", index=data.index)

        for i in range(1, len(data)):
            if pd.isna(short_sma.iloc[i]) or pd.isna(long_sma.iloc[i]):
                continue

            if pd.isna(short_sma.iloc[i - 1]) or pd.isna(long_sma.iloc[i - 1]):
                continue

            crossed_up = (
                short_sma.iloc[i - 1] <= long_sma.iloc[i - 1]
                and short_sma.iloc[i] > long_sma.iloc[i]
            )

            crossed_down = (
                short_sma.iloc[i - 1] >= long_sma.iloc[i - 1]
                and short_sma.iloc[i] < long_sma.iloc[i]
            )

            if crossed_up:
                signals.iloc[i] = "BUY"
            elif crossed_down:
                signals.iloc[i] = "SELL"

        return signals