# risk_return.py

import pandas as pd
import numpy as np

def load_price_data(file_path="data/stock_prices.csv"):
    data = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return data

def calculate_daily_returns(price_data):
    returns = price_data.pct_change().dropna()
    return returns

def calculate_annualized_metrics(daily_returns):
    mean_daily = daily_returns.mean()
    cov_daily = daily_returns.cov()

    mean_annual = mean_daily * 252
    std_annual = daily_returns.std() * np.sqrt(252)
    cov_annual = cov_daily * 252

    return mean_annual, std_annual, cov_annual

if __name__ == "__main__":
    prices = load_price_data()
    daily_returns = calculate_daily_returns(prices)
    mean_return, std_dev, cov_matrix = calculate_annualized_metrics(daily_returns)

    print("📈 Annualized Mean Returns:")
    print(mean_return)
    print("\n📊 Annualized Volatility (Standard Deviation):")
    print(std_dev)
    print("\n🔗 Annualized Covariance Matrix:")
    print(cov_matrix)
