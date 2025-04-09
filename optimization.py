# optimization.py

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from risk_return import load_price_data, calculate_daily_returns, calculate_annualized_metrics

def portfolio_performance(weights, mean_returns, cov_matrix):
    """
    Calculate expected return and volatility for a given set of weights.
    """
    returns = np.dot(weights, mean_returns)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return returns, volatility

def negative_sharpe_ratio(weights, mean_returns, cov_matrix, risk_free_rate=0.0):
    """
    The negative Sharpe ratio (since we'll minimize it).
    """
    returns, volatility = portfolio_performance(weights, mean_returns, cov_matrix)
    return -(returns - risk_free_rate) / volatility

def get_optimal_weights(mean_returns, cov_matrix, risk_free_rate=0.0):
    num_assets = len(mean_returns)
    initial_weights = np.ones(num_assets) / num_assets
    bounds = tuple((0, 1) for _ in range(num_assets))  # No short-selling
    constraints = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})  # Weights sum to 1

    result = minimize(negative_sharpe_ratio, initial_weights,
                      args=(mean_returns, cov_matrix, risk_free_rate),
                      method='SLSQP', bounds=bounds, constraints=constraints)

    return result.x

if __name__ == "__main__":
    prices = load_price_data()
    daily_returns = calculate_daily_returns(prices)
    mean_return, std_dev, cov_matrix = calculate_annualized_metrics(daily_returns)

    optimal_weights = get_optimal_weights(mean_return, cov_matrix)

    print("💡 Optimal Portfolio Weights (Max Sharpe Ratio):")
    for ticker, weight in zip(prices.columns, optimal_weights):
        print(f"{ticker}: {weight:.2%}")
