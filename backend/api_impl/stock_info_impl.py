from concurrent.futures import ThreadPoolExecutor
from api_impl import yfinance_impl

# Function to fetch data for a single stock ticker.
def fetch_single_stock_data(ticker):
    yfinance_output = yfinance_impl.YFinance(ticker)
    
    metrics = [
        "marketCap", "sector", "industry",
        "dividendYield", "trailingPE", "earningsQuarterlyGrowth",
        "currentPrice", "regularMarketVolume", "beta",
        "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "currency"
    ]
    
    stock_info = {metric: yfinance_output.info.get(metric, "N/A") for metric in metrics}
    stock_info["company_name"] = get_stock_name(ticker)
    
    # Create a dictionary to hold our chosen metrics for this stock.
    # If a metric is not available, we use "N/A" as a placeholder.
    return stock_info

# Define a function to fetch data for all listed stock tickers.
# TODO: Might be deleted in the future
def fetch_stock_data(tickers):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(fetch_single_stock_data, tickers))
    
    stock_data_dict = {}
    
    for result in results:
        stock_data_dict.update(result)

    return stock_data_dict

def get_stock_name(ticker):
    ticker_to_name = {
        "AAPL":"Apple",
        "MSFT":"Microsoft",
        "GOOGL":"Google",
        "AMZN":"Amazon",
        "META":"Meta",
        "BRK-B":"Berkshire Hathaway",
        "V":"Visa",
        "JNJ":"Johnson & Johnson",
        "WMT":"Walmart",
        "PG":"Procter & Gamble",
    }
    
    return ticker_to_name[ticker]

# Used for standalone testing, 
if __name__ == "__main__":
    print(fetch_single_stock_data('AAPL'))