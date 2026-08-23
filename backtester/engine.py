import pandas as pd

from backtester.data import load_stock_data
from backtester.portfolio import Portfolio
from backtester.metrics import total_return
from backtester.strategies import (
    BuyAndHoldStrategy,
    Strategy,
)


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

def compare_with_buy_and_hold(
    data: pd.DataFrame,
    strategy: Strategy,
    initial_capital: float
) -> dict:
    strategy_backtest = Backtest(
        data=data,
        strategy=strategy,
        initial_capital=initial_capital
    )

    buy_hold_backtest = Backtest(
        data=data,
        strategy=BuyAndHoldStrategy(),
        initial_capital=initial_capital
    )

    strategy_results = strategy_backtest.run()
    buy_hold_results = buy_hold_backtest.run()

    strategy_final = strategy_results["PortfolioValue"].iloc[-1]
    buy_hold_final = buy_hold_results["PortfolioValue"].iloc[-1]

    return {
        "strategy_final_value": strategy_final,
        "buy_hold_final_value": buy_hold_final,
        "strategy_return": total_return(
            initial_capital,
            strategy_final
        ),
        "buy_hold_return": total_return(
            initial_capital,
            buy_hold_final
        ),
    }

def compare_with_sp500(
    data: pd.DataFrame,
    strategy: Strategy,
    initial_capital: float,
    start: str,
    end: str
) -> dict:
    strategy_backtest = Backtest(
        data=data,
        strategy=strategy,
        initial_capital=initial_capital
    )

    strategy_results = strategy_backtest.run()

    sp500_data = load_stock_data(
        ticker="^GSPC",
        start=start,
        end=end
    )

    sp500_backtest = Backtest(
        data=sp500_data,
        strategy=BuyAndHoldStrategy(),
        initial_capital=initial_capital
    )

    sp500_results = sp500_backtest.run()

    strategy_final = strategy_results["PortfolioValue"].iloc[-1]
    sp500_final = sp500_results["PortfolioValue"].iloc[-1]

    return {
        "strategy_final_value": strategy_final,
        "sp500_final_value": sp500_final,
        "strategy_return": total_return(
            initial_capital,
            strategy_final
        ),
        "sp500_return": total_return(
            initial_capital,
            sp500_final
        ),
    }