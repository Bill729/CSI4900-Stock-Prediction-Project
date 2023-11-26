import numpy as np
from api_impl import tickers_impl
import yfinance as yf
from sklearn.metrics import mean_absolute_error, mean_squared_error

from models import stock_price_predictor as price_predictor

NUM_PREDICTED_DAYS = 7

def get_model_performance():
    tickers = tickers_impl.get_stock_tickers()
    data = yf.download(tickers, period="1y")['Close']
    
    test_dates = data.index.unique()[-NUM_PREDICTED_DAYS:]

    training_data = data[~data.index.isin(test_dates)]
    test_data = data[data.index.isin(test_dates)]

    stock_indicators = price_predictor.calculate_indicators(training_data, tickers)
    predicted_data = price_predictor.predict_for_n_days(stock_indicators, tickers, NUM_PREDICTED_DAYS)

    output = {}
    for day in range(NUM_PREDICTED_DAYS):
        actual_values = [test_data[ticker][day] for ticker in tickers]
        predicted_values = [predicted_data[ticker][day] for ticker in tickers]

        mae = mean_absolute_error(actual_values, predicted_values)
        mse = mean_squared_error(actual_values, predicted_values)
        rmse = np.sqrt(mse)

        output.setdefault(day+1, {})
        output[day+1]["MAE"] = mae
        output[day+1]["MSE"] = mse
        output[day+1]["RMSE"] = rmse
    
    return output
