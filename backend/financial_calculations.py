import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# List of stock ticker symbols that we're interested in.
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "BRK-B", "V", "JNJ", "WMT", "PG"]

# Define a function to fetch data for a single stock ticker.
def fetch_single_stock_data(ticker):

    # Create an object for the stock using yfinance's Ticker class.
    stock = yf.Ticker(ticker)
    
    # Fetch all available stock information.
    stock_info = stock.info
    
    # Define the specific metrics we want to extract.
    metrics = [
        "marketCap", "sector", "industry",
        "dividendYield", "trailingPE", "earningsQuarterlyGrowth",
        "currentPrice", "regularMarketVolume", "beta",
        "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "currency"
    ]
    
    # Create a dictionary to hold our chosen metrics for this stock.
    # If a metric is not available, we use "N/A" as a placeholder.
    return {ticker: {metric: stock_info.get(metric, "N/A") for metric in metrics}}

# Define a function to fetch data for all listed stock tickers.
def fetch_stock_data():

    # Use ThreadPoolExecutor to run multiple threads and speed up data fetching.
    with ThreadPoolExecutor() as executor:
        # Fetch the stock data asynchronously and convert the results to a list.
        results = list(executor.map(fetch_single_stock_data, tickers))
    
    # Initialize an empty dictionary to hold all stock data.
    stock_data_dict = {}
    
    # Populate the stock_data_dict with data fetched by all threads.
    for result in results:
        stock_data_dict.update(result)

    # Return the dictionary containing all stock data.
    return stock_data_dict

# Define a function to calculate stock indicators for a single stock ticker.
def calculate_single_indicator(ticker, close_prices):

    # Calculate Simple Moving Average (SMA) over a 20-day window.
    sma = close_prices[ticker].rolling(window=20).mean()
    
    # Calculate Exponential Moving Average (EMA) over a 20-day window.
    ema = close_prices[ticker].ewm(span=20).mean()
    
    # Calculate Standard Deviation over a 20-day window.
    rolling_std = close_prices[ticker].rolling(window=20).std()
    
    # Calculate the upper and lower Bollinger Bands.
    upper_band = sma + (rolling_std * 2)
    lower_band = sma - (rolling_std * 2)
    
    # Calculate the daily price change.
    delta = close_prices[ticker].diff()
    
    # Calculate the gain and loss components of RSI.
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    
    # Calculate Relative Strength (RS).
    rs = gain / loss
    
    # Calculate Relative Strength Index (RSI).
    rsi = 100 - (100 / (1 + rs))
    
    # Calculate MACD and Signal line indicators.
    short_ema = close_prices[ticker].ewm(span=12).mean()
    long_ema = close_prices[ticker].ewm(span=26).mean()
    macd = short_ema - long_ema
    signal_line = macd.ewm(span=9).mean()

    # Compile all these indicators into a single DataFrame.
    return pd.DataFrame({
        f'{ticker}_SMA': sma,
        f'{ticker}_EMA': ema,
        f'{ticker}_Upper_Band': upper_band,
        f'{ticker}_Lower_Band': lower_band,
        f'{ticker}_RSI': rsi,
        f'{ticker}_MACD': macd,
        f'{ticker}_Signal_Line': signal_line
    })

# Define a function to calculate stock indicators for all listed stock tickers.
def calculate_indicators():

    # Download historical stock data for all tickers for the past 1 year.
    data = yf.download(tickers, period="1y")
    
    # Extract only the 'Close' prices from the downloaded data.
    close_prices = data['Close']
    
    # Use ThreadPoolExecutor to speed up the indicator calculations.
    with ThreadPoolExecutor() as executor:
        # Calculate the indicators for all stock tickers.
        indicators_list = list(executor.map(lambda ticker: calculate_single_indicator(ticker, close_prices), tickers))

    # Combine the calculated indicators for all tickers into a single DataFrame.
    indicators_df = pd.concat(indicators_list, axis=1)
    indicators_df = indicators_df.iloc[19:]

    # Return the DataFrame containing all the calculated indicators.
    return indicators_df

# Used for standalone testing, 
if __name__ == "__main__":
    stock_data = fetch_stock_data()
    stock_indicators = calculate_indicators()
    print(stock_indicators)
    print(stock_data)