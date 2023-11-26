import yfinance as yf

from api_impl import tickers_impl
from models import stock_price_predictor as price_predictor

# Train model without the latest 7 days
tickers = tickers_impl.get_stock_tickers()
data = yf.download(tickers, period="1y")['Close']
excluded_dates = data.index.unique()[-7:]
training_data = data[~data.index.isin(excluded_dates)]

stock_indicators = price_predictor.calculate_indicators(training_data, tickers)
price_predictor.train_LSTM_models(stock_indicators, tickers)

# TODO: Train model with all the data. We might need to modify model implementation so that we can save multiple models at the same time
# Suggestion: directory should be backend/models/models/week_old_models/ and backend/models/current_models