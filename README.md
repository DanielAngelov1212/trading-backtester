# Trading Backtester

A Python application for backtesting stock trading strategies using historical market data.

The project allows users to test different trading strategies, evaluate their performance, and compare them with Buy & Hold and the S&P 500.

## Features

- Load historical stock data from Yahoo Finance
- Select a custom backtesting period
- Set initial portfolio capital
- Simulate buying and selling stocks
- Test multiple trading strategies
- Calculate performance metrics
- Compare strategies with Buy & Hold
- Compare strategies with the S&P 500
- Interactive Streamlit dashboard
- REST API using FastAPI
- Automated tests with pytest

## Technical Indicators

The project implements the following technical indicators:

- Simple Moving Average (SMA)
- Exponential Moving Average (EMA)
- Relative Strength Index (RSI)
- Moving Average Convergence Divergence (MACD)

## Trading Strategies

The following strategies are available:

### Buy & Hold

Buys the selected stock at the beginning of the simulation and holds the position for the entire period.

### Moving Average Crossover

Uses a short-term and long-term moving average.

- BUY when the short moving average crosses above the long moving average
- SELL when the short moving average crosses below the long moving average

### RSI Strategy

Uses the Relative Strength Index to identify potentially overbought and oversold conditions.

- BUY when RSI is below the oversold threshold
- SELL when RSI is above the overbought threshold

### MACD Strategy

Uses the MACD line and signal line.

- BUY when MACD crosses above the signal line
- SELL when MACD crosses below the signal line

## Performance Metrics

The backtester calculates:

- Final Portfolio Value
- Total Return
- Maximum Drawdown
- Sharpe Ratio

The selected strategy is also compared against:

- Buy & Hold on the selected stock
- Buy & Hold on the S&P 500

## Project Structure

```text
trading-backtester/
│
├── app.py
├── api.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── backtester/
│   ├── __init__.py
│   ├── data.py
│   ├── indicators.py
│   ├── strategies.py
│   ├── portfolio.py
│   ├── engine.py
│   ├── metrics.py
│   └── exceptions.py
│
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_data.py
    ├── test_engine.py
    ├── test_indicators.py
    ├── test_metrics.py
    ├── test_portfolio.py
    └── test_strategies.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/DanielAngelov1212/trading-backtester.git
cd trading-backtester
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows:

```bash
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Streamlit Application

Start the graphical interface with:

```bash
streamlit run app.py
```

The application allows you to select:

- Stock ticker
- Trading strategy
- Start date
- End date
- Initial capital

After running the backtest, the dashboard displays performance metrics, a portfolio comparison chart, benchmark results, and generated trades.

## Running the API

Start the FastAPI server with:

```bash
uvicorn api:app --reload
```

The interactive API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## API

### POST /backtest

Runs a backtest using the provided parameters.

Example request:

```json
{
  "ticker": "AAPL",
  "strategy": "moving_average",
  "start": "2022-01-01",
  "end": "2025-01-01",
  "initial_capital": 10000
}
```

Example response:

```json
{
  "ticker": "AAPL",
  "strategy": "moving_average",
  "initial_capital": 10000,
  "final_value": 12000,
  "total_return": 20,
  "max_drawdown": -10,
  "sharpe_ratio": 1.2
}
```

Supported strategy names:

```text
buy_and_hold
moving_average
rsi
macd
```

## Running Tests

Run all automated tests with:

```bash
pytest
```

## Technologies

- Python
- pandas
- NumPy
- yfinance
- Streamlit
- Plotly
- FastAPI
- Uvicorn
- pytest