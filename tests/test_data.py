import pytest

from backtester.data import load_stock_data
from backtester.exceptions import (
    InvalidDateRangeError,
    InvalidTickerError,
)


def test_load_stock_data_returns_data():
    data = load_stock_data(
        ticker="AAPL",
        start="2024-01-01",
        end="2024-02-01"
    )

    assert not data.empty


def test_invalid_date_range():
    with pytest.raises(InvalidDateRangeError):
        load_stock_data(
            ticker="AAPL",
            start="2025-01-01",
            end="2024-01-01"
        )


def test_invalid_ticker():
    with pytest.raises(InvalidTickerError):
        load_stock_data(
            ticker="THIS_IS_NOT_A_REAL_TICKER_123",
            start="2024-01-01",
            end="2024-02-01"
        )