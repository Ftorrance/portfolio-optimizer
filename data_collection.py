

# data_collection.py

import yfinance as yf
import pandas as pd

def download_stock_data(tickers, start_date, end_date, file_path="data/stock_prices.csv"):
    """
    Download adjusted closing prices (or close prices if adjusted not available) and save to CSV.
    """
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)['Close']
    data.to_csv(file_path)
    print(f"✅ Stock data saved to {file_path}")

if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']  # Customize your list
    start_date = "2020-01-01"
    end_date = "2024-12-31"

    download_stock_data(tickers, start_date, end_date)
