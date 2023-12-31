from concurrent.futures import ThreadPoolExecutor
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout, Bidirectional, BatchNormalization
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
from keras.optimizers import Adam
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras import backend as K
import tensorflow as tf
import yfinance as yf
import numpy as np
import pandas as pd
import os

LEARNING_RATE = 0.005
EPOCHS = 200
BATCH_SIZE = 64

# Define a function to calculate stock indicators for a single stock ticker.
# TODO: Add this to the output of get_stock_info
def calculate_single_indicator(ticker, close_prices):

    # Check if close_prices is a DataFrame or a Series
    if isinstance(close_prices, pd.DataFrame):
        # If it's a DataFrame, check if ticker is in columns
        if ticker in close_prices.columns:
            price_data = close_prices[ticker]
        else:
            raise ValueError(f'Ticker {ticker} not found in DataFrame columns.')
    elif isinstance(close_prices, pd.Series):
        # If it's a Series, use it directly as the price data
        price_data = close_prices
    else:
        raise TypeError('close_prices must be either a pandas DataFrame or Series.')
    
    indicators = {}  # Initialize an empty dictionary to collect the indicators

    # Update the dictionary for each metric
    indicators[f'{ticker}_SMA'] = price_data.rolling(window=20).mean()
    indicators[f'{ticker}_EMA'] = price_data.ewm(span=20).mean()
    rolling_std = price_data.rolling(window=20).std()
    indicators[f'{ticker}_Upper_Band'] = indicators[f'{ticker}_SMA'] + (rolling_std * 2)
    indicators[f'{ticker}_Lower_Band'] = indicators[f'{ticker}_SMA'] - (rolling_std * 2)
    delta = price_data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    indicators[f'{ticker}_RSI'] = 100 - (100 / (1 + rs))
    short_ema = price_data.ewm(span=12).mean()
    long_ema = price_data.ewm(span=26).mean()
    indicators[f'{ticker}_MACD'] = short_ema - long_ema
    indicators[f'{ticker}_Signal_Line'] = indicators[f'{ticker}_MACD'].ewm(span=9).mean()

    return pd.DataFrame(indicators)
# Define a function to calculate stock indicators for all listed stock tickers.
# TODO: Might be deleted in the future
def calculate_indicators(close_prices, tickers):

    # Handle the case when close_prices is a Series (single ticker)
    if isinstance(close_prices, pd.Series):
        close_prices = close_prices.to_frame(tickers[0])  # Convert to DataFrame with the ticker as column name

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

def create_sequences(data, n_steps=20):
    X, Y = [], []
    for i in range(len(data) - n_steps):
        # Create sequences of 'n_steps' length
        X.append(data[i:i + n_steps, :-1])
        Y.append(data[i + n_steps, 0])
    return np.array(X), np.array(Y)


# Function to train LSTM models for different stock tickers
def train_LSTM_models(indicators_df, tickers, save_dir, n_steps=20):
    # Callbacks for early stopping and learning rate reduction
    early_stopping = EarlyStopping(monitor='loss', patience=20)
    reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, min_lr=0.001)

    # Create and compile a base model outside the loop to be cloned later
    sample_ticker = tickers[0]  # Using the first ticker as a sample
    sample_df_ticker = indicators_df.filter(like=sample_ticker)
    sample_df_ticker_scaled = MinMaxScaler().fit_transform(sample_df_ticker)
    sample_shape = (n_steps, sample_df_ticker_scaled.shape[1] - 1)
    base_model = create_model(sample_shape)
    base_optimizer = Adam(learning_rate=LEARNING_RATE)
    base_model.compile(optimizer=base_optimizer, loss='mean_squared_error')
    
    for ticker in tickers:
        print(f"Training model_{ticker}")
        df_ticker = indicators_df.filter(like=ticker)
        if df_ticker.isnull().values.any():
            print(f"Found null values in {ticker}'s indicators. Skipping training.")
            continue
        
        model = tf.keras.models.clone_model(base_model)
        optimizer = Adam(learning_rate=LEARNING_RATE)
        model.compile(optimizer=optimizer, loss='mean_squared_error')
        
        scaler = MinMaxScaler(feature_range=(0, 1))
        df_ticker_scaled = scaler.fit_transform(df_ticker)
        X, Y = create_sequences(df_ticker_scaled, n_steps)
        
        model.fit(X, Y, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.2, callbacks=[early_stopping, reduce_lr])
        
        model_path = get_model_path(ticker, save_dir)
        model.save(model_path)
        K.clear_session()

# Function to make predictions with trained LSTM models for different stock tickers
# def predict_with_LSTM(indicators_df, tickers, n_steps=20):
#     future_market_predictions = {}
    
#     for ticker in tickers:
#         try:
#             model_path = get_model_path(ticker)
#             model = load_model(model_path)
#             df_ticker = indicators_df.filter(like=ticker)
#             if df_ticker.isnull().values.any():
#                 continue
            
#             scaler = MinMaxScaler(feature_range=(0, 1))
#             df_ticker_scaled = scaler.fit_transform(df_ticker)
            
#             last_values_scaled = df_ticker_scaled[-n_steps:, :-1].reshape(1, n_steps, df_ticker_scaled.shape[1] - 1)
#             future_scaled = custom_predict(model, last_values_scaled)
            
#             future_unscaled = scaler.inverse_transform(
#                 np.hstack((future_scaled, np.zeros((future_scaled.shape[0], df_ticker_scaled.shape[1]-1))))
#             )
            
#             future_market_predictions[ticker] = future_unscaled[0, 0]
#         except IOError:
#             print(f"Model for {ticker} could not be found. Skipping prediction.")
#         finally:
#             K.clear_session()
    
#     return future_market_predictions


def predict_for_n_days(indicators_df, tickers, n_days, n_steps=20):
    future_market_predictions = {}

    for ticker in tickers:
        model_path = get_model_path(ticker)
        print(f"Predicting using model_{ticker}")
        try:
            model = load_model(model_path)
            df_ticker = indicators_df.filter(like=ticker)
            if df_ticker.isnull().values.any():
                continue

            scaler = MinMaxScaler(feature_range=(0, 1))
            df_ticker_scaled = scaler.fit_transform(df_ticker)
            column_names = df_ticker.columns  # Capture the column names

            # Initialize an array to hold the predictions for n days
            predictions = []

            for day in range(n_days):
                # Take the last n_steps data points for prediction
                last_n_steps = df_ticker.iloc[-n_steps:]
                last_values_scaled = scaler.transform(last_n_steps)

                # Reshape for the model
                last_values_scaled = last_values_scaled[:, :-1].reshape(1, n_steps, last_values_scaled.shape[1] - 1)
                future_scaled = custom_predict(model, last_values_scaled)

                # Inverse transform the prediction and append to predictions
                future_unscaled = scaler.inverse_transform(
                    np.hstack((future_scaled, np.zeros((future_scaled.shape[0], len(column_names)-1))))
                )
                next_day_prediction = future_unscaled[0, 0]
                predictions.append(next_day_prediction)

                # Update df_ticker with the new prediction for the next iteration
                new_row = pd.DataFrame([[next_day_prediction] + [0]*(len(column_names)-1)], columns=column_names)
                df_ticker = pd.concat([df_ticker, new_row], ignore_index=True)
            future_market_predictions[ticker] = predictions
        except IOError:
            print(f"Model for {ticker} could not be found in {model_path}. Skipping prediction.")
        finally:
            K.clear_session()
    
    return future_market_predictions

# def get_model_path(ticker):
#     model_path = f'\models\model_{ticker}'
#     current_dir_path = os.path.dirname(os.path.abspath(__file__))
#     absolute_path = current_dir_path + model_path
#     return absolute_path
def get_model_path(ticker, save_dir):
    model_path = os.path.join(save_dir, f'model_{ticker}')
    return model_path


# Used for standalone testing
if __name__ == "__main__":
    tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "BRK-B", "V", "WMT", "PG"][:2]
    data = yf.download(tickers, period="1y")
    close_prices = data['Close']
    stock_indicators = calculate_indicators(close_prices, tickers)
    # Train models (might be run less frequently, e.g., monthly)
    train_LSTM_models(stock_indicators, tickers)

    # Predict with the trained models (might be run daily)
    future_market_predictions = predict_for_n_days(stock_indicators, tickers, 1)
    print(future_market_predictions)
