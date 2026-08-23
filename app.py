import plotly.graph_objects as go
import streamlit as st

from backtester.data import load_stock_data
from backtester.engine import (
    Backtest,
    compare_all,
)
from backtester.exceptions import BacktestError
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


st.title("Trading Backtester")

ticker = st.text_input(
    "Stock ticker",
    value="AAPL"
)

strategy_name = st.selectbox(
    "Strategy",
    [
        "Buy and Hold",
        "Moving Average",
        "RSI",
        "MACD",
    ]
)

start_date = st.date_input(
    "Start date"
)

end_date = st.date_input(
    "End date"
)

initial_capital = st.number_input(
    "Initial capital",
    min_value=100.0,
    value=10000.0
)


if st.button("Run Backtest"):
    try:
        data = load_stock_data(
            ticker=ticker,
            start=str(start_date),
            end=str(end_date)
        )

        if strategy_name == "Buy and Hold":
            strategy = BuyAndHoldStrategy()

        elif strategy_name == "Moving Average":
            strategy = MovingAverageStrategy()

        elif strategy_name == "RSI":
            strategy = RSIStrategy()

        else:
            strategy = MACDStrategy()

        backtest = Backtest(
            data=data,
            strategy=strategy,
            initial_capital=initial_capital
        )

        results = backtest.run()

        final_value = results[
            "PortfolioValue"
        ].iloc[-1]

        return_value = total_return(
            initial_capital,
            final_value
        )

        drawdown = max_drawdown(
            results["PortfolioValue"]
        )

        sharpe = sharpe_ratio(
            results["PortfolioValue"]
        )

        risked_amount = risked_capital(
            backtest.portfolio.trades
        )

        risked_return = return_on_risked_capital(
            initial_capital,
            final_value,
            risked_amount
        )

        st.subheader("Strategy Results")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Final Value",
            f"${final_value:.2f}"
        )

        col2.metric(
            "Total Return",
            f"{return_value:.2f}%"
        )

        col3.metric(
            "Max Drawdown",
            f"{drawdown:.2f}%"
        )

        col4.metric(
            "Sharpe Ratio",
            f"{sharpe:.2f}"
        )

        risk_col1, risk_col2 = st.columns(2)

        risk_col1.metric(
            "Risked Capital",
            f"${risked_amount:.2f}"
        )

        risk_col2.metric(
            "Return on Risked Capital",
            f"{risked_return:.2f}%"
        )

        comparison = compare_all(
            data=data,
            strategy=strategy,
            initial_capital=initial_capital,
            start=str(start_date),
            end=str(end_date)
        )

        st.subheader("Portfolio Performance Comparison")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=comparison["buy_hold_results"].index,
                y=comparison[
                    "buy_hold_results"
                ]["PortfolioValue"],
                mode="lines",
                name="Buy & Hold",
                line=dict(
                    color="green",
                    width=2
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=comparison["sp500_results"].index,
                y=comparison[
                    "sp500_results"
                ]["PortfolioValue"],
                mode="lines",
                name="S&P 500",
                line=dict(
                    color="orange",
                    width=2
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=comparison["strategy_results"].index,
                y=comparison[
                    "strategy_results"
                ]["PortfolioValue"],
                mode="lines",
                name="Strategy",
                line=dict(
                    color="blue",
                    width=3,
                    dash="dash"
                )
            )
        )

        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Portfolio Value ($)",
            hovermode="x unified",
            legend_title="Portfolio",
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.subheader("Benchmark Comparison")

        benchmark_col1, benchmark_col2, benchmark_col3 = (
            st.columns(3)
        )

        benchmark_col1.metric(
            "Strategy Return",
            f"{comparison['strategy_return']:.2f}%"
        )

        benchmark_col2.metric(
            "Buy & Hold Return",
            f"{comparison['buy_hold_return']:.2f}%"
        )

        benchmark_col3.metric(
            "S&P 500 Return",
            f"{comparison['sp500_return']:.2f}%"
        )

        st.subheader("Trades")

        trades = results[
            results["Signal"] != "HOLD"
        ]

        st.dataframe(trades)

    except BacktestError as error:
        st.error(str(error))

    except ValueError as error:
        st.error(str(error))

    except Exception as error:
        st.error(
            f"Unexpected error: {error}"
        )