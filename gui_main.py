# gui_main.py

import tkinter as tk
from tkinter import messagebox
from risk_return import load_price_data, calculate_daily_returns, calculate_annualized_metrics
from optimization import get_optimal_weights
from visualization import simulate_random_portfolios, plot_efficient_frontier
from benchmark_comparison import download_benchmark_data, calculate_portfolio_value, plot_comparison
from data_collection import download_stock_data
import os

def ensure_data_folder():
    if not os.path.exists("data"):
        os.makedirs("data")

def show_weights_popup(tickers, weights):
    popup = tk.Toplevel()
    popup.title("Optimal Portfolio Weights")
    popup.geometry("300x300")
    
    text = tk.Text(popup, wrap="word")
    text.insert(tk.END, "✅ Optimal Portfolio Weights:\n\n")
    for ticker, weight in zip(tickers, weights):
        text.insert(tk.END, f"{ticker}: {weight:.2%}\n")
    text.pack(expand=True, fill="both")

    tk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

def run_analysis():
    tickers = ticker_entry.get().upper().split(',')
    start_date = start_entry.get()
    end_date = end_entry.get()

    if not tickers or not start_date or not end_date:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    try:
        ensure_data_folder()

        # Step 1: Download & prepare data
        download_stock_data(tickers, start_date, end_date)
        prices = load_price_data()
        daily_returns = calculate_daily_returns(prices)
        mean_return, std_dev, cov_matrix = calculate_annualized_metrics(daily_returns)

        # Step 2: Optimize
        optimal_weights = get_optimal_weights(mean_return, cov_matrix)

        # Step 3: Show weights popup
        show_weights_popup(tickers, optimal_weights)

        # Step 4: Graphs
        results = simulate_random_portfolios(5000, mean_return, cov_matrix)
        plot_efficient_frontier(results, optimal_weights, mean_return, cov_matrix)

        benchmark = download_benchmark_data(start=start_date, end=end_date)
        portfolio_value = calculate_portfolio_value(prices, optimal_weights)
        plot_comparison(portfolio_value, benchmark)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# 🖼️ GUI setup
root = tk.Tk()
root.title("Portfolio Optimization Tool")
root.geometry("400x250")

tk.Label(root, text="Stock Tickers (comma-separated):").pack(pady=5)
ticker_entry = tk.Entry(root, width=40)
ticker_entry.pack()

tk.Label(root, text="Start Date (YYYY-MM-DD):").pack(pady=5)
start_entry = tk.Entry(root, width=20)
start_entry.pack()

tk.Label(root, text="End Date (YYYY-MM-DD):").pack(pady=5)
end_entry = tk.Entry(root, width=20)
end_entry.pack()

tk.Button(root, text="Run Optimization", command=run_analysis).pack(pady=15)

root.mainloop()
