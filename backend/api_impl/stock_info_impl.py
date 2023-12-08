from concurrent.futures import ThreadPoolExecutor
import yfinance as yf

# Function to fetch data for a single stock ticker.
def fetch_single_stock_data(ticker):
    yfinance_output = yf.Ticker(ticker)
    
    metrics = [
        "marketCap", "sector", "industry",
        "dividendYield", "trailingPE", "earningsQuarterlyGrowth",
        "currentPrice", "regularMarketVolume", "beta",
        "fiftyTwoWeekLow", "fiftyTwoWeekHigh", "currency"
    ]
    
    stock_info = {metric: yfinance_output.info.get(metric, "N/A") for metric in metrics}
    stock_info["companyName"] = get_stock_name(ticker)
    
    return stock_info

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