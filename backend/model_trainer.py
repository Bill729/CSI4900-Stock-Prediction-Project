import yfinance as yf
import os

from api_impl import tickers_impl
from models import stock_price_predictor as price_predictor

def train_and_save_model(data, tickers, model_dir):
    # Calculate stock indicators
    stock_indicators = price_predictor.calculate_indicators(data, tickers)
    
    # Train LSTM models
    # Ensure train_LSTM_models function in price_predictor accepts save_dir and saves models to this directory
    price_predictor.train_LSTM_models(stock_indicators, tickers, save_dir=model_dir)

# Get stock tickers
tickers = tickers_impl.get_stock_tickers()

# Download data for the past year
data = yf.download(tickers, period="1y")['Close']

# Train model excluding the latest 7 days
excluded_dates = data.index.unique()[-7:]
training_data = data[~data.index.isin(excluded_dates)]

# Directory for models trained without the latest 7 days
week_old_model_dir = 'backend/models/week_old_models/'
os.makedirs(week_old_model_dir, exist_ok=True)
train_and_save_model(training_data, tickers, week_old_model_dir)

# Train model with all data
# Directory for models trained with all data
current_model_dir = 'backend/models/current_models/'
os.makedirs(current_model_dir, exist_ok=True)
train_and_save_model(data, tickers, current_model_dir)
