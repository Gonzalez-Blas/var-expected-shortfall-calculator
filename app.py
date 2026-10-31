import streamlit as st
import yfinance as yf
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

st.title("📈 Quantitative Portfolio VaR & ES Dashboard")

# Interactive Sidebar Controls
ticker_input = st.sidebar.text_input("Enter Tickers (comma separated):", "AAPL, MSFT, GOOGL, SPY")
confidence = st.sidebar.slider("Confidence Level (%)", 90.0, 99.9, 95.0) / 100.0

tickers = [t.strip() for t in ticker_input.split(",")]

if st.button("Calculate Risk Metrics"):
    df = yf.download(tickers, start="2020-01-01", progress=False)
    data = df["Adj Close"] if "Adj Close" in df.columns else df["Close"]
    returns = data.pct_change().dropna()
    
    # Equal weight allocation
    weights = np.ones(len(tickers)) / len(tickers)
    portfolio_returns = (returns * weights).sum(axis=1)
    
    # Risk Metrics
    var_hist = np.percentile(portfolio_returns, (1 - confidence) * 100)
    es_hist = portfolio_returns[portfolio_returns <= var_hist].mean()
    
    # Display Key Metrics
    col1, col2 = st.columns(2)
    col1.metric("Historical VaR", f"{var_hist:.2%}")
    col2.metric("Expected Shortfall (ES)", f"{es_hist:.2%}")
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.histplot(portfolio_returns, bins=50, kde=True, ax=ax, color="skyblue")
    ax.axvline(var_hist, color="red", linestyle="--", label=f"VaR ({var_hist:.2%})")
    ax.axvline(es_hist, color="darkred", linestyle=":", label=f"ES ({es_hist:.2%})")
    ax.set_title("Portfolio Loss Distribution")
    ax.legend()
    st.pyplot(fig)
