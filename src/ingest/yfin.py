# yfin.py
# Yahoo Finance fetch

import yfinance as yf
import pandas as pd

def fetch_stock_data(ticker: str, period="1y", interval="1d"):
    """
    Fetch stock price data from Yahoo Finance.
    """
    try:
        df = yf.download(ticker, period=period, interval=interval)
        return df.reset_index()
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return pd.DataFrame()

