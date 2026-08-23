import pytest

from backtester.portfolio import Portfolio


def test_portfolio_initial_state():
    portfolio = Portfolio(1000)

    assert portfolio.initial_capital == 1000
    assert portfolio.cash == 1000
    assert portfolio.shares == 0
    assert portfolio.trades == []


def test_buy():
    portfolio = Portfolio(1000)

    portfolio.buy(100)

    assert portfolio.cash == 0
    assert portfolio.shares == 10

    assert len(portfolio.trades) == 1
    assert portfolio.trades[0]["action"] == "BUY"


def test_buy_keeps_remaining_cash():
    portfolio = Portfolio(1000)

    portfolio.buy(300)

    assert portfolio.shares == 3
    assert portfolio.cash == 100


def test_sell():
    portfolio = Portfolio(1000)

    portfolio.buy(100)
    portfolio.sell(120)

    assert portfolio.shares == 0
    assert portfolio.cash == 1200

    assert len(portfolio.trades) == 2
    assert portfolio.trades[1]["action"] == "SELL"


def test_portfolio_value():
    portfolio = Portfolio(1000)

    portfolio.buy(100)

    value = portfolio.get_value(120)

    assert value == 1200


def test_invalid_initial_capital():
    with pytest.raises(ValueError):
        Portfolio(0)


def test_invalid_price():
    portfolio = Portfolio(1000)

    with pytest.raises(ValueError):
        portfolio.buy(-10)