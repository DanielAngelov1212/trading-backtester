import pandas as pd
import yfinance as yf


def load_stock_data(
    ticker: str,
    start: str,
    end: str
) -> pd.DataFrame:
    data = yf.download(
        ticker,
        start=start,
        end=end,
        progress=False
    )

    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    return data