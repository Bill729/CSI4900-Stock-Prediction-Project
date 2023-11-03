from concurrent.futures import ThreadPoolExecutor
import yfinance as yf


# Function to fetch data for a single stock ticker.
def fetch_single_stock_data(ticker):
    stock = yf.Ticker(ticker)
    
    stock_info = stock.info
    
    metrics = [
        "marketCap", "sector", "industry",
        "dividendYield", "trailingPE", "earningsQuarterlyGrowth",
        "currentPrice", "regularMarketVolume", "beta",
        "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "currency"
    ]
    
    # Create a dictionary to hold our chosen metrics for this stock.
    # If a metric is not available, we use "N/A" as a placeholder.
    return {metric: stock_info.get(metric, "N/A") for metric in metrics}

# Define a function to fetch data for all listed stock tickers.
# TODO: Might be deleted in the future
def fetch_stock_data(tickers):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_single_stock_data, tickers))
    
    stock_data_dict = {}
    
    for result in results:
        stock_data_dict.update(result)

    return stock_data_dict

# Used for standalone testing, 
if __name__ == "__main__":
    print(fetch_single_stock_data('AAPL'))