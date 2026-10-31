# 📈 Value at Risk (VaR) & Expected Shortfall (ES) Calculator

A quantitative financial risk management tool built in Python to evaluate tail risk for single assets and multi-asset portfolios using Historical Simulation, Parametric Estimation, and Monte Carlo approaches.

---

## 📌 Project Overview & Risk Theory

When managing stock portfolios, measuring average returns isn't enough—investors need to understand their **maximum potential losses during extreme market downturns**. This calculator computes two essential risk management metrics required by financial institutions and regulators:

1. **Value at Risk (VaR):**
   * **Definition:** Measures the maximum expected percentage loss over a given time horizon at a specific confidence level (e.g., 95%).
   * **Interpretation:** A 95% 1-day VaR of `-2.50%` indicates that on 95% of trading days, portfolio losses will not exceed 2.50%. There is only a 5% chance of exceeding this loss threshold.

2. **Expected Shortfall (ES) / Conditional VaR (CVaR):**
   * **Definition:** Measures the average loss on days when losses surpass the VaR cutoff line.
   * **Interpretation:** While VaR tells you where the bad days start, ES answers: *"When extreme market crashes occur, how severe will the average loss actually be?"*

---

## 🚀 Features

- **Multi-Asset Support:** Analyzes custom portfolio ticker combinations with adjustable asset weights.
- **Dynamic Market Data:** Fetches live historical daily prices dynamically via `yfinance`.
- **Multiple Risk Models:** Evaluates risk using **Historical Simulation** and **Parametric (Variance-Covariance)** methods.
- **VaR Backtesting:** Evaluates past portfolio performance against predicted risk limits to count model violations over time.
- **Interactive Web App:** Includes a Streamlit dashboard (`app.py`) for custom real-time parameter tweaking.

---

## 🛠️ Project Structure

```text
.
├── app.py                      # Interactive Streamlit dashboard
├── var_calculator.py           # Core single-asset VaR/ES script
├── var_calculator_advanced.py  # Multi-asset & backtesting engine
├── requirements.txt            # Python dependencies
├── project_guide.jpg           # Reference roadmap image
└── README.md                   # Project documentation
