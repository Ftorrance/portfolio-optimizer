# visualization.py

import numpy as np
import matplotlib.pyplot as plt
from risk_return import load_price_data, calculate_daily_returns, calculate_annualized_metrics
from optimization import get_optimal_weights, portfolio_performance

def simulate_random_portfolios(num_portfolios, mean_returns, cov_matrix, risk_free_rate=0.0):
    results = {
        "returns": [],
        "volatility": [],
        "sharpe_ratio": [],
        "weights": []
    }

    num_assets = len(mean_returns)

    for _ in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)

        ret, vol = portfolio_performance(weights, mean_returns, cov_matrix)
        sharpe = (ret - risk_free_rate) / vol

        results["returns"].append(ret)
        results["volatility"].append(vol)
        results["sharpe_ratio"].append(sharpe)
        results["weights"].append(weights)

    return results

def plot_efficient_frontier(results, optimal_weights, mean_returns, cov_matrix):
    returns = results["returns"]
    volatility = results["volatility"]
    sharpe_ratio = results["sharpe_ratio"]

    opt_return, opt_volatility = portfolio_performance(optimal_weights, mean_returns, cov_matrix)

    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(volatility, returns, c=sharpe_ratio, cmap='viridis', alpha=0.7)
    plt.colorbar(scatter, label="Sharpe Ratio")

    plt.scatter(opt_volatility, opt_return, c='red', marker='*', s=200, label='Optimal Portfolio')
    plt.xlabel('Volatility (Standard Deviation)')
    plt.ylabel('Expected Return')
    plt.title('Efficient Frontier with Optimal Portfolio')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    prices = load_price_data()
    daily_returns = calculate_daily_returns(prices)
    mean_return, std_dev, cov_matrix = calculate_annualized_metrics(daily_returns)

    results = simulate_random_portfolios(5000, mean_return, cov_matrix)
    optimal_weights = get_optimal_weights(mean_return, cov_matrix)

    plot_efficient_frontier(results, optimal_weights, mean_return, cov_matrix)
