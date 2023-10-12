# Import necessary libraries.
import yfinance as yf  # For fetching financial data.
import pandas as pd  # For data manipulation and analysis.
import numpy as np  # For numerical operations.

def calculate_indicators():
    # Define the stock tickers for the top 10 S&P 500 companies.
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "BRK-B", "V", "JNJ", "WMT", "PG"]

    # Fetch historical stock data for these tickers for the past 1 year.
    data = yf.download(tickers, period="1y")

    # Extract the 'Close' prices from the fetched data.
    close_prices = data['Close']

    # Perform basic statistical analysis on the close prices.
    # Get summary statistics like mean, median, etc.
    stats_summary = close_prices.describe()

    # Calculate the mean of the close prices.
    mean = close_prices.mean()

    # Calculate the median of the close prices.
    median = close_prices.median()

    # Calculate the standard deviation of the close prices.
    std_dev = close_prices.std()

    # Calculate the variance of the close prices.
    variance = close_prices.var()

    # Calculate the correlation matrix to understand relationships between different stocks.
    correlation_matrix = close_prices.corr()

    # Initialize an empty DataFrame to hold all the calculated financial indicators.
    indicators_df = pd.DataFrame()

    # Loop through each stock ticker to calculate financial indicators
    for ticker in tickers:
        # Calculate 20-day Simple Moving Average (SMA).
        # SMA is the average stock price over the last 'n' days. It's used to identify trends.
        sma = close_prices[ticker].rolling(window=20).mean()
        
        # Calculate 20-day Exponential Moving Average (EMA).
        # EMA is similar to SMA but gives more weight to recent prices. Useful for tracking short-term price movements.
        ema = close_prices[ticker].ewm(span=20).mean()
        
        # Calculate Bollinger Bands.
        # Upper and Lower Bollinger Bands are used to identify the volatility and direction of price movement.
        # They are two standard deviations away from the SMA.
        rolling_std = close_prices[ticker].rolling(window=20).std()
        upper_band = sma + (rolling_std * 2)  # Upper Bollinger Band.
        lower_band = sma - (rolling_std * 2)  # Lower Bollinger Band.
        
        # Calculate Relative Strength Index (RSI).
        # RSI is a momentum indicator that measures the speed and change of price movements.
        # RSI ranges from 0 to 100. Generally, an RSI above 70 indicates an overbought condition, while an RSI below 30 indicates an oversold condition.
        delta = close_prices[ticker].diff()  # Calculate price change.
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()  # Average gain over 14 days
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()  # Average loss over 14 days
        rs = gain / loss  # Calculate Relative Strength (RS).
        rsi = 100 - (100 / (1 + rs))  # Calculate RSI.
        
        # Calculate Moving Average Convergence Divergence (MACD).
        # MACD is a trend-following momentum indicator, showing the relationship between two EMAs of a security’s price.
        # The MACD is calculated by subtracting the 26-day EMA from the 12-day EMA.
        short_ema = close_prices[ticker].ewm(span=12).mean()  # Short-term EMA.
        long_ema = close_prices[ticker].ewm(span=26).mean()  # Long-term EMA.
        macd = short_ema - long_ema  # MACD line.
        signal_line = macd.ewm(span=9).mean()  # Signal line.
        
        # Store these indicators in a DataFrame.
        indicators = pd.DataFrame({
            f'{ticker}_SMA': sma,
            f'{ticker}_EMA': ema,
            f'{ticker}_Upper_Band': upper_band,
            f'{ticker}_Lower_Band': lower_band,
            f'{ticker}_RSI': rsi,
            f'{ticker}_MACD': macd,
            f'{ticker}_Signal_Line': signal_line
        })
        
        # Add the indicators for this stock to the master DataFrame.
        indicators_df = pd.concat([indicators_df, indicators], axis=1)

    # Drop the rows that don't have all indicators calculated (first 19 rows).
    indicators_df = indicators_df.iloc[19:]

    # Return the DataFrame with all the indicators.
    return indicators_df
