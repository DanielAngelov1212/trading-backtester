from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Trading Backtester API"
    }


def test_backtest_endpoint():
    response = client.post(
        "/backtest",
        json={
            "ticker": "AAPL",
            "strategy": "buy_and_hold",
            "start": "2024-01-01",
            "end": "2024-02-01",
            "initial_capital": 10000
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["ticker"] == "AAPL"
    assert data["strategy"] == "buy_and_hold"
    assert "final_value" in data
    assert "total_return" in data
    assert "max_drawdown" in data
    assert "sharpe_ratio" in data
    assert "risked_capital" in data
    assert "return_on_risked_capital" in data


def test_invalid_strategy():
    response = client.post(
        "/backtest",
        json={
            "ticker": "AAPL",
            "strategy": "unknown_strategy",
            "start": "2024-01-01",
            "end": "2024-02-01",
            "initial_capital": 10000
        }
    )

    assert response.status_code == 400
