# benchmark_comparison.py

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from risk_return import load_price_data, calculate_daily_returns, calculate_annualized_metrics
from optimization import get_optimal_weights

def download_benchmark_data(ticker='SPY', start="2020-01-01", end="2024-12-31"):
    benchmark = yf.download(ticker, start=start, end=end, auto_adjust=True)['Close']
    return benchmark

def calculate_portfolio_value(prices, weights):
    """
    Simulates portfolio value over time using fixed weights.
    """
    normalized = prices / prices.iloc[0]  # Normalize to 1
    portfolio = (normalized * weights).sum(axis=1)
    return portfolio

def plot_comparison(portfolio, benchmark):
    plt.figure(figsize=(10, 6))
    plt.plot(portfolio, label="Optimized Portfolio")
    plt.plot(benchmark / benchmark.iloc[0], label="Benchmark (SPY)", linestyle='--')
    plt.title("Portfolio vs Benchmark Performance")
    plt.xlabel("Date")
    plt.ylabel("Normalized Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    prices = load_price_data()
    daily_returns = calculate_daily_returns(prices)
    mean_return, std_dev, cov_matrix = calculate_annualized_metrics(daily_returns)

    # Optimize portfolio
    optimal_weights = get_optimal_weights(mean_return, cov_matrix)

    # Simulate portfolio value
    portfolio_value = calculate_portfolio_value(prices, optimal_weights)

    # Download benchmark (SPY)
    benchmark_value = download_benchmark_data(start=prices.index[0].strftime('%Y-%m-%d'),
                                               end=prices.index[-1].strftime('%Y-%m-%d'))

    # Plot both
    plot_comparison(portfolio_value, benchmark_value)
