import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from fredapi import Fred

# Set the page title
st.title("Portfolio Optimization App")

# Sidebar for user inputs
st.sidebar.header("User Input Parameters")

# Function to get user input
def get_user_input():
    tickers = st.sidebar.text_input("Enter stock tickers separated by commas", "SPY,BND,GLD,QQQ,VTI").split(',')
    start_date = st.sidebar.date_input("Select start date", datetime(2014, 1, 1))
    max_weight_constraint = st.sidebar.slider("Max Weight Constraint", 0.0, 1.0, 0.5, step=0.05)
    return tickers, start_date, max_weight_constraint

# Get user input
tickers, start_date, max_weight_constraint = get_user_input()

# Define end date
end_date = datetime.today()

# Display the selected parameters
st.write("### Selected Parameters")
selected_parameters_df = pd.DataFrame({
    "Parameter": ["Tickers", "Start Date", "End Date", "Max Weight Constraint"],
    "Value": [', '.join(tickers), start_date, end_date.date(), max_weight_constraint]
})
st.table(selected_parameters_df)

# Function to download adjusted close prices
def download_data(tickers, start_date, end_date):
    adj_close_df = pd.DataFrame()
    errors = []
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty:
                errors.append(ticker)
            else:
                adj_close_df[ticker] = data['Adj Close']
        except Exception as e:
            errors.append(ticker)
    return adj_close_df, errors

# Download data
adj_close_df, errors = download_data(tickers, start_date, end_date)

# Display error message if there are invalid tickers
if errors:
    st.error(f"The following tickers are invalid or have no data for the selected date range: {', '.join(errors)}")
    st.warning("Please enter valid stock tickers and ensure the date range includes data for the selected tickers.")
else:
    # Calculating the Daily Returns via Log Normal Returns
    log_returns = np.log(adj_close_df / adj_close_df.shift(1))
    log_returns = log_returns.dropna()

    # Calculate Covariance Matrix
    cov_matrix = log_returns.cov() * 252

    # Calculate the Portfolio Standard Deviation
    def standardDeviation(weights, cov_matrix):
        variance = weights.T @ cov_matrix @ weights
        return np.sqrt(variance)

    # Calculate Expected Return
    def expectedReturn(weights, log_returns):
        return np.sum(log_returns.mean() * weights * 252)

    # Calculate the Sharpe Ratio
    def sharpeRatio(weights, log_returns, cov_matrix, risk_free_rate):
        return (expectedReturn(weights, log_returns) - risk_free_rate) / standardDeviation(weights, cov_matrix)

    # Federal Reserve API (replace with your actual API key)
    fred = Fred(api_key='78c18ee9847b04540b6b63c52f29815a')
    ten_year_treasury_rate = fred.get_series_latest_release('GS10') / 100

    # Set the risk-free rate
    risk_free_rate = ten_year_treasury_rate.iloc[-1]

    # Define the function to minimize (negative Sharpe Ratio)
    def negSharpeRatio(weights, log_returns, cov_matrix, risk_free_rate):
        return -sharpeRatio(weights, log_returns, cov_matrix, risk_free_rate)

    # Set the constraints and bounds
    constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
    bounds = [(0, max_weight_constraint) for _ in range(len(tickers))]  # Adjusted for user input

    # Set the initial weights
    initialWeights = np.array([1 / len(tickers)] * len(tickers))

    # Optimize the weights to maximize Sharpe Ratio
    optimizedResults = minimize(negSharpeRatio, initialWeights, args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)
    optimialWeights = optimizedResults.x

    # Display analytics of the optimal portfolio
    st.write("### Optimal Portfolio Weights")
    optimal_weights_df = pd.DataFrame({'Ticker': tickers, 'Weight': optimialWeights})
    st.table(optimal_weights_df)

    optimalPortfolioReturn = expectedReturn(optimialWeights, log_returns)
    optimalPortfolioVolatility = standardDeviation(optimialWeights, cov_matrix)
    optimalSharpeRatio = sharpeRatio(optimialWeights, log_returns, cov_matrix, risk_free_rate)

    st.write("### Portfolio Performance Metrics")
    performance_metrics_df = pd.DataFrame({
        "Metric": ["Expected Annual Return", "Expected Volatility", "Sharpe Ratio"],
        "Value": [f"{optimalPortfolioReturn:.4f}", f"{optimalPortfolioVolatility:.4f}", f"{optimalSharpeRatio:.4f}"]
    })
    st.table(performance_metrics_df)

    # Display the optimal weights as a bar chart
    st.write("### Optimal Portfolio Weights Distribution")
    fig, ax = plt.subplots()
    ax.bar(tickers, optimialWeights, color='skyblue')
    ax.set_xlabel('Assets')
    ax.set_ylabel('Optimal Weights')
    ax.set_title('Optimal Portfolio Weights')
    st.pyplot(fig)

    # Display stock performance over time
    st.write("### Stock Performance Over Time")
    plt.figure(figsize=(10, 6))
    for ticker in adj_close_df.columns:
        plt.plot(adj_close_df.index, adj_close_df[ticker], label=ticker)
    plt.xlabel("Date")
    plt.ylabel("Adjusted Close Price")
    plt.title("Stock Performance")
    plt.legend()
    st.pyplot(plt)
