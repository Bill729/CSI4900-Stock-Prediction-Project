import yfinance as yf
from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

from models import stock_price_predictor as price_predictor

NUM_PREDICTED_DAYS = 7

def get_stock_prices(ticker):
    stock_prices = {}
    stock_prices['historical'] = get_historical_prices(ticker)
    stock_prices['predicted'] = get_predicted_prices(ticker)
    stock_prices['performance'] = get_price_performances(stock_prices['historical'], stock_prices['predicted'])
    
    # Add current date's price to predicted values for visual improvement
    today_epoch = max(stock_prices['historical'])
    stock_prices['predicted'][today_epoch] = stock_prices['historical'][today_epoch]
    
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

def get_price_performances(historical_prices, predicted_prices):
    
    today_epoch = max(historical_prices)
    today_date = datetime.utcfromtimestamp(today_epoch)
    
    one_week_ago_epoch = calculate_epoch(today_date, relativedelta(weeks=1))
    one_month_ago_epoch = calculate_epoch(today_date, relativedelta(months=1))
    three_months_ago_epoch = calculate_epoch(today_date, relativedelta(months=3))
    one_year_ago_epoch = calculate_epoch(today_date, relativedelta(years=1))
    oldest_epoch = min(historical_prices)
    newest_predicted_epoch = max(predicted_prices)
    
    today_price = get_price(historical_prices, today_epoch)
    one_week_old_price = get_price(historical_prices, one_week_ago_epoch)
    one_month_old_price = get_price(historical_prices, one_month_ago_epoch)
    three_month_old_price = get_price(historical_prices, three_months_ago_epoch)
    one_year_old_price = get_price(historical_prices, one_year_ago_epoch)
    oldest_price = get_price(historical_prices, oldest_epoch)
    newest_predicted_price = get_price(predicted_prices, newest_predicted_epoch)
    
    price_performance = {}
    price_performance['1w'] = calculate_performance(today_price, one_week_old_price)
    price_performance['1m'] = calculate_performance(today_price, one_month_old_price)
    price_performance['3m'] = calculate_performance(today_price, three_month_old_price)
    price_performance['1y'] = calculate_performance(today_price, one_year_old_price)
    price_performance['all'] = calculate_performance(today_price, oldest_price)
    price_performance['1w_predicted'] = calculate_performance(newest_predicted_price, today_price)
    
    return price_performance
    
def calculate_performance(curr_price, old_price):
    return (curr_price - old_price) / old_price * 100

def calculate_epoch(today_date, relative_delta):
    old_date = today_date - relative_delta
    return calendar.timegm(old_date.utctimetuple())

def get_price(prices_map, epoch):
    closest_epoch = min(prices_map.keys(), key=lambda x: abs(x - epoch))
    return prices_map[closest_epoch]


# Used for standalone testing, 
if __name__ == "__main__":
    print(get_stock_prices("AAPL")['performance'])
    