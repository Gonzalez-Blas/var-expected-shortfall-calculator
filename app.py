import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="VaR & ES Risk Calculator", layout="wide")

st.title("📈 Quantitative Portfolio Risk Dashboard")
st.markdown("Measure Value at Risk (VaR) and Expected Shortfall (ES) for custom stock portfolios.")

# Sidebar Settings
st.sidebar.header("Portfolio Settings")
ticker_input = st.sidebar.text_input("Tickers (comma-separated):", "AAPL, MSFT, GOOGL, SPY")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
confidence_pct = st.sidebar.slider("Confidence Level (%)", 90.0, 99.9, 95.0, step=0.5)
confidence = confidence_pct / 100.0

# Parse Tickers
tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]

if st.sidebar.button("Calculate Risk Metrics", type="primary") or st.session_state.get("ran", False):
    st.session_state["ran"] = True
    
    if not tickers:
        st.error("Please enter at least one valid ticker symbol.")
    else:
        with st.spinner("Fetching market data..."):
            df = yf.download(tickers, start=start_date, progress=False)
            
            # Handle Single vs Multi Ticker Downloads
            if "Adj Close" in df.columns:
                data = df["Adj Close"]
            elif "Close" in df.columns:
                data = df["Close"]
            else:
                data = df
            
            # Squeeze single-column DataFrames if needed
            if isinstance(data, pd.Series):
                data = data.to_frame()

        if data.empty:
            st.error("No data fetched. Please check the ticker symbols and date range.")
        else:
            # Daily Returns
            returns = data.pct_change().dropna()
            
            # Equal Weights
            weights = np.ones(len(data.columns)) / len(data.columns)
            portfolio_returns = (returns * weights).sum(axis=1)

            # Calculations
            var_hist = np.percentile(portfolio_returns, (1 - confidence) * 100)
            es_hist = portfolio_returns[portfolio_returns <= var_hist].mean()

            mean_ret = np.mean(portfolio_returns)
            std_ret = np.std(portfolio_returns)
            var_param = stats.norm.ppf(1 - confidence, mean_ret, std_ret)

            # Metrics Row
            col1, col2, col3, col4 = st.columns(4)
            col1.metric(f"Historical VaR ({confidence_pct:.1f}%)", f"{var_hist:.2%}")
            col2.metric(f"Historical ES ({confidence_pct:.1f}%)", f"{es_hist:.2%}")
            col3.metric(f"Parametric VaR ({confidence_pct:.1f}%)", f"{var_param:.2%}")
            col4.metric("Daily Volatility", f"{std_ret:.2%}")

            st.divider()

            # Visualizations
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.histplot(portfolio_returns, bins=50, kde=True, color="skyblue", ax=ax)
            ax.axvline(var_hist, color="red", linestyle="--", label=f"Hist VaR ({var_hist:.2%})")
            ax.axvline(es_hist, color="darkred", linestyle=":", label=f"Hist ES ({es_hist:.2%})")
            ax.axvline(var_param, color="orange", linestyle="--", label=f"Param VaR ({var_param:.2%})")
            ax.set_title(f"Portfolio Loss Distribution ({', '.join(tickers)})")
            ax.set_xlabel("Daily Returns")
            ax.set_ylabel("Frequency")
            ax.legend()
            st.pyplot(fig)
