import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Fetch Historical Data
ticker = "LSEG"
data = yf.download(ticker, start="2020-01-01", end="2024-01-01")["Adj Close"]

# 2. Calculate Daily Returns
returns = data.pct_change().dropna()

# 3. Compute Value at Risk (VaR)
confidence_level = 0.95
var_95 = np.percentile(returns, (1 - confidence_level) * 100)

# 4. Compute Expected Shortfall (ES)
es_95 = returns[returns <= var_95].mean()

print(f"Daily VaR (95%): {var_95:.4%}")
print(f"Daily Expected Shortfall (95%): {es_95:.4%}")

# 5. Plot Loss Distribution
plt.figure(figsize=(10, 6))
sns.histplot(returns, bins=50, kde=True, color="skyblue")
plt.axvline(var_95, color="red", linestyle="--", label=f"VaR 95% ({var_95:.2%})")
plt.axvline(es_95, color="darkred", linestyle=":", label=f"ES 95% ({es_95:.2%})")
plt.title(f"Portfolio Loss Distribution & Risk Metrics ({ticker})")
plt.xlabel("Daily Returns")
plt.ylabel("Frequency")
plt.legend()
plt.tight_layout()
plt.savefig("distribution_plot.png")
