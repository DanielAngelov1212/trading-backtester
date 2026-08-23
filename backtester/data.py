from datetime import datetime

import pandas as pd
import yfinance as yf

from backtester.exceptions import (
    InvalidDateRangeError,
    InvalidTickerError,
)


def load_stock_data(
    ticker: str,
    start: str,
    end: str
) -> pd.DataFrame:
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    if start_date >= end_date:
        raise InvalidDateRangeError(
            "Start date must be before end date."
        )

    data = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False
    )

    if data.empty:
        raise InvalidTickerError(
            f"No data found for ticker '{ticker}'."
        )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data
