from abc import ABC, abstractmethod
from backtester.indicators import sma, rsi, macd

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

class RSIStrategy(Strategy):

    def __init__(
        self,
        period: int = 14,
        oversold: float = 30,
        overbought: float = 70
    ) -> None:
        if period <= 0:
            raise ValueError("Period must be positive.")

        if not 0 <= oversold < overbought <= 100:
            raise ValueError("Invalid RSI thresholds.")

        self.period = period
        self.oversold = oversold
        self.overbought = overbought

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        rsi_values = rsi(data["Close"], self.period)

        signals = pd.Series("HOLD", index=data.index)

        for i in range(len(data)):
            if pd.isna(rsi_values.iloc[i]):
                continue

            if rsi_values.iloc[i] < self.oversold:
                signals.iloc[i] = "BUY"

            elif rsi_values.iloc[i] > self.overbought:
                signals.iloc[i] = "SELL"

        return signals

class MACDStrategy(Strategy):

    def __init__(
        self,
        short_period: int = 12,
        long_period: int = 26,
        signal_period: int = 9
    ) -> None:
        if short_period <= 0 or long_period <= 0 or signal_period <= 0:
            raise ValueError("Periods must be positive.")

        if short_period >= long_period:
            raise ValueError(
                "Short period must be smaller than long period."
            )

        self.short_period = short_period
        self.long_period = long_period
        self.signal_period = signal_period

    def generate_signals(self, data: pd.DataFrame) -> pd.Series:
        macd_line, signal_line = macd(
            data["Close"],
            short_period=self.short_period,
            long_period=self.long_period,
            signal_period=self.signal_period,
        )

        signals = pd.Series("HOLD", index=data.index)

        for i in range(1, len(data)):
            crossed_up = (
                macd_line.iloc[i - 1] <= signal_line.iloc[i - 1]
                and macd_line.iloc[i] > signal_line.iloc[i]
            )

            crossed_down = (
                macd_line.iloc[i - 1] >= signal_line.iloc[i - 1]
                and macd_line.iloc[i] < signal_line.iloc[i]
            )

            if crossed_up:
                signals.iloc[i] = "BUY"

            elif crossed_down:
                signals.iloc[i] = "SELL"

        return signals