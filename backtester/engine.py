import pandas as pd

from backtester.portfolio import Portfolio
from backtester.strategies import Strategy


class Backtest:

    def __init__(
        self,
        data: pd.DataFrame,
        strategy: Strategy,
        initial_capital: float
    ) -> None:
        if data.empty:
            raise ValueError("Data cannot be empty.")

        self.data = data
        self.strategy = strategy
        self.portfolio = Portfolio(initial_capital)

    def run(self) -> pd.DataFrame:
        signals = self.strategy.generate_signals(self.data)

        results = self.data.copy()
        results["Signal"] = signals
        results["PortfolioValue"] = 0.0

        for i in range(len(results)):
            price = float(results["Close"].iloc[i])
            signal = results["Signal"].iloc[i]

            if signal == "BUY":
                self.portfolio.buy(price)

            elif signal == "SELL":
                self.portfolio.sell(price)

            results.loc[
                results.index[i],
                "PortfolioValue"
            ] = self.portfolio.get_value(price)

        return results