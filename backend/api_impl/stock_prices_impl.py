import yfinance as yf

from models import stock_price_predictor as price_predictor

NUM_PREDICTED_DAYS = 7

def get_stock_prices(ticker):
    data = yf.download(ticker, period="max")
    stock_prices = {}
    stock_prices['historical'] = get_historical_prices(ticker)
    stock_prices['predicted'] = get_predicted_prices(ticker)
    print(stock_prices)
    return stock_prices
    
def get_historical_prices(ticker):
    data = yf.download(ticker, period="max")
    historical_prices = data['Close'].to_dict()
    formatted_prices = {int(date.timestamp()): price for date, price in historical_prices.items()}
    return formatted_prices
    
def get_predicted_prices(ticker):
    data = yf.download([ticker], period="1y")['Close']
    stock_indicators = price_predictor.calculate_indicators(data, [ticker])
    predicted_prices = price_predictor.predict_for_n_days(stock_indicators, [ticker], NUM_PREDICTED_DAYS)[ticker]
    
    latest_date = data.index.max()
    latest_epoch = int(latest_date.timestamp())
    
    output = {}
    for i in range(len(predicted_prices)):
        latest_epoch += 86400
        output[latest_epoch] = predicted_prices[i]
    
    return output

# Used for standalone testing, 
if __name__ == "__main__":
    get_stock_prices("AAPL")