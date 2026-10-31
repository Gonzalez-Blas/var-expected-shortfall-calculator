# Value at Risk (VaR) & Expected Shortfall (ES) Calculator

A Python-based financial risk management tool designed to measure portfolio tail risk using historical simulation.

## Features
- Fetches real-time market data via `yfinance`.
- Calculates daily historical returns and summary statistics.
- Computes **Value at Risk (VaR)** and **Expected Shortfall (ES)** at 95% confidence intervals.
- Visualizes return distributions with clear risk metrics.

## Setup & Execution
Run in Google Colab or locally:
```bash
pip install -r requirements.txt
python var_calculator.py
