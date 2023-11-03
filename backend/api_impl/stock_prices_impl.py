import yfinance as yf
import time

def get_stock_prices(ticker):
    data = yf.download(ticker, period="max")
    stock_prices = {}
    stock_prices['historical'] = get_historical_prices(ticker)
    stock_prices['predicted'] = get_predicted_prices(ticker)    
    return stock_prices
    
def get_historical_prices(ticker):
    data = yf.download(ticker, period="max")
    historical_prices = data['Close'].to_dict()
    formatted_prices = {int(date.timestamp()): price for date, price in historical_prices.items()}
    return formatted_prices
    
def get_predicted_prices(ticker):
    # TODO: Utilize model
    epoch = str(int(time.time()))
    predictions = {'AAPL': 130.96765194318883, 'MSFT': 235.1904937933153, 'GOOGL': 88.80080867493501, 'AMZN': 86.24289496189886, 'META': 108.36334946044701, 'BRK-B': 303.47671262653034, 'V': 207.2184004897953, 'JNJ': 152.94026889224082, 'WMT': 139.61731202224806, 'PG': 138.85857541690805}
    predicted_prices = {epoch:predictions[ticker]}
    return predicted_prices

# Used for standalone testing, 
if __name__ == "__main__":
    get_stock_prices("AAPL")