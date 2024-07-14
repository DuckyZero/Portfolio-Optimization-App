import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

# Define Tickers and Time Range
tickers = ['SPY', 'BND', 'GLD', 'QQQ', 'VTI']
# Initialize trading days to annualize calculations
TRADING_DAYS = 252

end_date = datetime.today()
# start date to 10 years ago
start_date = end_date - timedelta(days=10*365)
#print(start_date)

# Download Adjusted Close Prices
adj_close_df = pd.DataFrame()
for ticker in tickers:
    data = yf.download(ticker, start=start_date, end=end_date)
    adj_close_df[ticker] = data['Adj Close']

#(adj_close_df)

# Calculating the Daily Returns via Log Normal Returns
log_returns = np.log(adj_close_df / adj_close_df.shift(1))
# Drops missing values
log_returns = log_returns.dropna()

# Calculate Covariance Matrix
# How we measure the total risk of the portfolio
# We multiply by 252 to annualize the value
cov_matrix = log_returns.cov()*TRADING_DAYS
print(cov_matrix)

# Calculate the Portfolio Standard Deviation
def standardDeviation(weights, cov_matrix):
    variance = weights.T @ cov_matrix @ weights
    return np.sqrt(variance)

# Calculate Expected Return
# Assumption: Expected returns are based on historical returns
def expectedReturn(weights, log_returns):
    return np.sum(log_returns.mean()*weights*TRADING_DAYS)

# Calculate the Sharpe Ratio
# Sharpe Ratio = Portfolio Return - Risk Free Rate / Standard Deviation
def sharpeRatio(weights, log_returns, cov_matrix, risk_free_rate):
    return(expectedReturn(weights, log_returns) - risk_free_rate) / standardDeviation(weights, cov_matrix)

# Federal Reserve API
from fredapi import Fred
fred = Fred(api_key='78c18ee9847b04540b6b63c52f29815a')
ten_year_treasury_rate = fred.get_series_latest_release('GS10') / 100

# Set the risk-free rate
risk_free_rate = ten_year_treasury_rate.iloc[-1]
print(risk_free_rate)


# Define the function to minimize (negative Sharpe Ratio)
# In the case the scipy.optimize() function, there is no direct method to find the maximum value of a function
def negSharpeRatio(weights, log_returns, cov_matrix, risk_free_rate):
    return -sharpeRatio(weights, log_returns, cov_matrix, risk_free_rate)

# Set the constraints and bounds:
# Constraints: the sum of all portfolio weigfhts must equal to 1
# 'EQ' = equality constraint, 'fun' = function check_sum
constraints = {'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1}
# setting 0 means we cannot go short in any asset, or sell any assets we do not own. Meaning, we will only go long or purchase assets
# 0.5 we cannot have 50% of our portfolio in any particular security
bounds = [(0,0.5) for _ in range(len(tickers))]

# Set the initial weights
initialWeights = np.array([1/len(tickers)]*len(tickers))
print(initialWeights)

# Optimize the weights to maximize Sharpe Ratio
# SLSQP stands for Sequential Least Squares Quadratic Progrmaming, which is a numerical optimization technique suitable for solving nonlinear optimization problems with constraints
optimizedResults = minimize(negSharpeRatio, initialWeights, args=(log_returns, cov_matrix, risk_free_rate), method='SLSQP', constraints=constraints, bounds=bounds)

# Get optimial weights
# .x allows us to access the results
optimialWeights = optimizedResults.x

# ---- Analyze the Optimal Portfolio ----
# Display analytics of the optimal portfolio
print("Optimal Weights:")
for ticker, weight in zip(tickers, optimialWeights):
    print(f"{ticker}: {weight:.4f}")
print()
optimalPortfolioReturn = expectedReturn(optimialWeights, log_returns)
optimalPortfolioVolatility = standardDeviation(optimialWeights, cov_matrix)
optimalSharpeRatio = sharpeRatio(optimialWeights, log_returns, cov_matrix, risk_free_rate)

print(f"Expected Annual Return: {optimalPortfolioReturn:.4f}")
print(f"Expcted Volatility: {optimalPortfolioVolatility:.4f}")
print(f"Sharpe Ratio: {optimalSharpeRatio:.4f}")


# ---- Display Final Portfolio ----

# Create a bar char of the optimial weights
plt.figure(figsize=(10,6))
plt.bar(tickers, optimialWeights)

# Add labels and titles
plt.xlabel('Assets')
plt.ylabel('Optimal Weights')
plt.title('Optimal Portfolio Weights')

# Display the chart
plt.show()
