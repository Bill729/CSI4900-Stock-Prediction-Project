import yfinance as yf
import pandas as pd
import numpy as np

# Tickers with the actual tickers of the top 10 S&P 500 companies.
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "BRK-B", "V", "JNJ", "WMT", "PG"]

# Fetch data for all tickers
data = yf.download(tickers, period="1y")

# Extracting Close prices for each stock
close_prices = data['Close']

# Basic Statistical Analysis
stats_summary = close_prices.describe()

# Calculate mean
mean = close_prices.mean()

# Calculate median
median = close_prices.median()

# Calculate standard deviation
std_dev = close_prices.std()

# Calculate variance
variance = close_prices.var()

# Calculate correlation matrix
correlation_matrix = close_prices.corr()

# Calculate Simple Moving Average (SMA) dynamically based on available data
sma = close_prices.expanding(min_periods=1).mean()

# Calculate Exponential Moving Average (EMA) with adjust=True
ema = close_prices.ewm(span=14, adjust=True).mean()

# Dynamic Bollinger Bands
rolling_mean = close_prices.expanding(min_periods=1).mean()
rolling_std = close_prices.expanding(min_periods=1).std()
upper_band = rolling_mean + (rolling_std * 2)
lower_band = rolling_mean - (rolling_std * 2)

# Dynamic RSI
delta = close_prices.diff(1)
gain = delta.where(delta > 0, 0).expanding(min_periods=1).mean()
loss = -delta.where(delta < 0, 0).expanding(min_periods=1).mean()
rs = gain / loss
rsi = 100 - (100 / (1 + rs))

# Dynamic MACD
exp12 = close_prices.ewm(span=12, adjust=True).mean()
exp26 = close_prices.ewm(span=26, adjust=True).mean()
macd = exp12 - exp26
signal = macd.ewm(span=9, adjust=True).mean()
macd_histogram = macd - signal

indicators_dict = {
    'Close': close_prices,
    'SMA': sma,
    'EMA': ema,
    'Upper Bollinger Band': upper_band,
    'Lower Bollinger Band': lower_band,
    'RSI': rsi,
    'MACD': macd,
    'Signal Line': signal,
    'MACD Histogram': macd_histogram
}

# Print indicators
for key, value in indicators_dict.items():
    print(f"{key}:\n{value.head()}\n")

