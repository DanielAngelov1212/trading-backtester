from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from backtester.data import load_stock_data
from backtester.engine import Backtest
from backtester.metrics import (
    max_drawdown,
    return_on_risked_capital,
    risked_capital,
    sharpe_ratio,
    total_return,
)
from backtester.strategies import (
    BuyAndHoldStrategy,
    MACDStrategy,
    MovingAverageStrategy,
    RSIStrategy,
)


app = FastAPI(
    title="Trading Backtester API"
)


class BacktestRequest(BaseModel):
    ticker: str
    strategy: str
    start: str
    end: str
    initial_capital: float


@app.get("/")
def root():
    return {
        "message": "Trading Backtester API"
    }


@app.post("/backtest")
def run_backtest(request: BacktestRequest):
    try:
        data = load_stock_data(
            ticker=request.ticker,
            start=request.start,
            end=request.end
        )

        if request.strategy == "buy_and_hold":
            strategy = BuyAndHoldStrategy()

        elif request.strategy == "moving_average":
            strategy = MovingAverageStrategy()

        elif request.strategy == "rsi":
            strategy = RSIStrategy()

        elif request.strategy == "macd":
            strategy = MACDStrategy()

        else:
            raise ValueError(
                "Unknown strategy."
            )

        backtest = Backtest(
            data=data,
            strategy=strategy,
            initial_capital=request.initial_capital
        )

        results = backtest.run()

        final_value = float(
            results["PortfolioValue"].iloc[-1]
        )

        risked_amount = risked_capital(
            backtest.portfolio.trades
        )

        risked_return = return_on_risked_capital(
            request.initial_capital,
            final_value,
            risked_amount
        )

        return {
            "ticker": request.ticker,
            "strategy": request.strategy,
            "initial_capital": request.initial_capital,
            "final_value": final_value,
            "total_return": total_return(
                request.initial_capital,
                final_value
            ),
            "risked_capital": risked_amount,
            "return_on_risked_capital": risked_return,
            "max_drawdown": max_drawdown(
                results["PortfolioValue"]
            ),
            "sharpe_ratio": sharpe_ratio(
                results["PortfolioValue"]
            ),
        }

    except Exception as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )