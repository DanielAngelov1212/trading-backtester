import numpy as np
import pandas as pd


def total_return(
    initial_capital: float,
    final_value: float
) -> float:
    return (
        (final_value - initial_capital)
        / initial_capital
    ) * 100


def max_drawdown(
    portfolio_values: pd.Series
) -> float:
    running_max = portfolio_values.cummax()

    drawdown = (
        portfolio_values - running_max
    ) / running_max

    return drawdown.min() * 100


def sharpe_ratio(
    portfolio_values: pd.Series
) -> float:
    returns = portfolio_values.pct_change().dropna()

    if returns.empty or returns.std() == 0:
        return 0.0

    return (
        returns.mean()
        / returns.std()
    ) * np.sqrt(252)