from abc import ABC, abstractmethod

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