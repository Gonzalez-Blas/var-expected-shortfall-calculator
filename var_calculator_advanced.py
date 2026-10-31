import yfinance as yf
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# 1. Multi-Asset Portfolio Setup
# ==========================================
tickers = ["AAPL", "MSFT", "GOOGL", "SPY"]
weights = np.array([0.3, 0.3, 0.2, 0.2])  # Must sum to 1.0

# Fetch historical data
df = yf.download(tickers, start="2020-01-01", end="2026-10-30", progress=False)

# Extract prices safely
data = df["Adj Close"] if "Adj Close" in df.columns else df["Close"]

# Calculate individual daily returns & weighted portfolio returns
returns = data.pct_change().dropna()
portfolio_returns = (returns * weights).sum(axis=1)

# ==========================================
# 2. Historical vs. Parametric VaR & ES
# ==========================================
confidence = 0.95

# Historical Simulation Method
var_hist = np.percentile(portfolio_returns, (1 - confidence) * 100)
es_hist = portfolio_returns[portfolio_returns <= var_hist].mean()

# Parametric (Variance-Covariance) Method
mean = np.mean(portfolio_returns)
std_dev = np.std(portfolio_returns)
var_param = stats.norm.ppf(1 - confidence, mean, std_dev)

# Parametric ES calculation
z_score = stats.norm.ppf(1 - confidence)
es_param = mean - (std_dev * stats.norm.pdf(z_score) / (1 - confidence))

print("=== RISK METRICS (95% Confidence) ===")
print(f"Historical VaR: {var_hist:.4%} | Historical ES: {es_hist:.4%}")
print(f"Parametric VaR: {var_param:.4%} | Parametric ES: {es_param:.4%}\n")

# ==========================================
# 3. VaR Backtesting Engine
# ==========================================
# Count days where actual portfolio loss exceeded predicted VaR threshold
exceptions = portfolio_returns[portfolio_returns < var_hist]
num_exceptions = len(exceptions)
total_days = len(portfolio_returns)
exception_rate = num_exceptions / total_days
expected_rate = 1 - confidence

print("=== BACKTEST RESULTS ===")
print(f"Total Trading Days Analyzed: {total_days}")
print(f"VaR Violations (Actual Loss > VaR): {num_exceptions} days")
print(f"Observed Violation Rate: {exception_rate:.2%} (Expected: {expected_rate:.2%})")

# ==========================================
# 4. Visualization & Reporting
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Plot 1: Portfolio Loss Distribution
sns.histplot(portfolio_returns, bins=60, kde=True, color="skyblue", ax=axes[0])
axes[0].axvline(var_hist, color="red", linestyle="--", label=f"Hist VaR ({var_hist:.2%})")
axes[0].axvline(es_hist, color="darkred", linestyle=":", label=f"Hist ES ({es_hist:.2%})")
axes[0].axvline(var_param, color="orange", linestyle="--", label=f"Param VaR ({var_param:.2%})")
axes[0].set_title("Portfolio Return Distribution & Tail Risk Thresholds")
axes[0].set_xlabel("Daily Returns")
axes[0].set_ylabel("Frequency")
axes[0].legend()

# Plot 2: Time-Series Backtesting (Returns vs. VaR Cutoff)
axes[1].plot(portfolio_returns.index, portfolio_returns, label="Daily Portfolio Return", alpha=0.6, color="navy")
axes[1].axhline(var_hist, color="red", linestyle="--", label=f"95% VaR Threshold ({var_hist:.2%})")
axes[1].scatter(exceptions.index, exceptions, color="crimson", zorder=5, label="VaR Violations")
axes[1].set_title("VaR Backtest: Daily Returns vs. Risk Limit Over Time")
axes[1].set_xlabel("Date")
axes[1].set_ylabel("Daily Return")
axes[1].legend()

plt.tight_layout()
plt.savefig("portfolio_risk_report.png")
plt.show()
