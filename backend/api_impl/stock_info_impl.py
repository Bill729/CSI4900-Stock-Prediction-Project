import yfinance as yf
import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor
from tickers_impl import get_stock_tickers
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Bidirectional, BatchNormalization
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
from keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from tensorflow.keras import backend as K
import tensorflow as tf


LEARNING_RATE = 0.005
EPOCHS = 200
BATCH_SIZE = 64

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

# Define a function to calculate stock indicators for a single stock ticker.
# TODO: Add this to the output of get_stock_info
def calculate_single_indicator(ticker, close_prices):

    indicators = {}  # Initialize an empty dictionary to collect the indicators

    # Update the dictionary for each metric
    indicators[f'{ticker}_SMA'] = close_prices[ticker].rolling(window=20).mean()
    indicators[f'{ticker}_EMA'] = close_prices[ticker].ewm(span=20).mean()
    rolling_std = close_prices[ticker].rolling(window=20).std()
    indicators[f'{ticker}_Upper_Band'] = indicators[f'{ticker}_SMA'] + (rolling_std * 2)
    indicators[f'{ticker}_Lower_Band'] = indicators[f'{ticker}_SMA'] - (rolling_std * 2)
    delta = close_prices[ticker].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    indicators[f'{ticker}_RSI'] = 100 - (100 / (1 + rs))
    short_ema = close_prices[ticker].ewm(span=12).mean()
    long_ema = close_prices[ticker].ewm(span=26).mean()
    indicators[f'{ticker}_MACD'] = short_ema - long_ema
    indicators[f'{ticker}_Signal_Line'] = indicators[f'{ticker}_MACD'].ewm(span=9).mean()

    return pd.DataFrame(indicators)
# Define a function to calculate stock indicators for all listed stock tickers.
# TODO: Might be deleted in the future
def calculate_indicators(close_prices, tickers):

    # Download historical stock data for all tickers for the past 1 year.
    data = yf.download(tickers, period="1y")

    # Select only the 'Close' columns
    close_prices = data['Close']

    with ThreadPoolExecutor() as executor:
        indicators_list = list(executor.map(lambda ticker: calculate_single_indicator(ticker, close_prices), tickers))

    indicators_df = pd.concat(indicators_list, axis=1)
    indicators_df = indicators_df.iloc[19:]  # Remove rows with NaN (due to rolling operations)

    return indicators_df

def create_model(input_shape):
    model = Sequential()
    # Adding two Bidirectional LSTM layers with BatchNormalization and Dropout
    for _ in range(2):
        model.add(Bidirectional(LSTM(100, return_sequences=True, activation='tanh'), input_shape=input_shape))
        model.add(BatchNormalization())
        model.add(Dropout(0.3))
    # Adding a final Bidirectional LSTM layer and BatchNormalization
    model.add(Bidirectional(LSTM(100, activation='tanh')))
    model.add(BatchNormalization())
    # Output layer with one neuron
    model.add(Dense(1))
    return model

# TensorFlow function for making predictions with the model; decorated to reduce retracing
@tf.function(experimental_relax_shapes=True, reduce_retracing=True)
def custom_predict(model, input_data):
    return model(input_data, training=False)



# Function to train LSTM models for different stock tickers and make future predictions
def train_and_predict_LSTM(indicators_df, tickers):
    future_market_predictions = {}
    
    # Callbacks for early stopping and learning rate reduction
    early_stopping = EarlyStopping(monitor='loss', patience=20)
    reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, min_lr=0.001)

    # Create and compile a base model outside the loop to be cloned later
    sample_ticker = tickers[0]  # Using the first ticker as a sample
    sample_df_ticker = indicators_df.filter(like=sample_ticker)
    sample_df_ticker_scaled = MinMaxScaler().fit_transform(sample_df_ticker)
    sample_shape = (1, sample_df_ticker_scaled.shape[1])
    base_model = create_model(sample_shape)
    base_optimizer = Adam(learning_rate=LEARNING_RATE)
    base_model.compile(optimizer=base_optimizer, loss='mean_squared_error')
    
    # Loop over each stock ticker
    for ticker in tickers:
        
        df_ticker = indicators_df.filter(like=ticker)
        
        # Skip if there are any null values
        if df_ticker.isnull().values.any():
            continue
        
        # Clone the base model and compile it
        model = tf.keras.models.clone_model(base_model)
        optimizer = Adam(learning_rate=LEARNING_RATE)
        model.compile(optimizer=optimizer, loss='mean_squared_error')
        
        # Data scaling and preparation
        scaler = MinMaxScaler(feature_range=(0, 1))
        df_ticker_scaled = scaler.fit_transform(df_ticker)
        X, Y = create_sequences(df_ticker_scaled)  # Assumed function; modify accordingly
        
        # Train the model
        model.fit(X, Y, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.2, callbacks=[early_stopping, reduce_lr])
        
        # Make predictions on the last available data point
        last_values_scaled = df_ticker_scaled[-1].reshape(1, -1)
        last_values_scaled = np.reshape(last_values_scaled, (last_values_scaled.shape[0], 1, last_values_scaled.shape[1]))
        future_scaled = custom_predict(model, last_values_scaled)
        
        # Inverse scale the prediction
        future_unscaled = scaler.inverse_transform(np.hstack((future_scaled, np.zeros((future_scaled.shape[0], df_ticker_scaled.shape[1]-1)))))
        
        # Store the prediction
        future_market_predictions[ticker] = future_unscaled[0, 0]
        
        # Clear the Keras session
        K.clear_session()
        
    return future_market_predictions

# Used for standalone testing, 
if __name__ == "__main__":
    tickers = get_stock_tickers()  # Assumed to be a list of tickers
    stock_data = fetch_stock_data(tickers)
    data = yf.download(tickers, period="1y")
    close_prices = data['Close']
    stock_indicators = calculate_indicators(close_prices, tickers)
    future_market_predictions = train_and_predict_LSTM(stock_indicators, tickers)
    print(future_market_predictions)