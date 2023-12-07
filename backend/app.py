from datetime import date
import os
import shelve
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from api_impl import stock_info_impl, tickers_impl, stock_prices_impl, stock_news_impl, model_perf_impl

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

shelve_lock = threading.Lock()

'''
Returns a list of all tickers we are tracking (Feature 1)
'''
@app.route('/tickers', methods=['GET'])
def get_stock_tickers():
    api_impl = tickers_impl.get_stock_tickers
    return get_data(request.path, api_impl)


'''
Returns the model's performance information
Returns a map of maps that contains the MSE, RMSE and MAE of the prediction of a specific date
'''
@app.route('/model/performance', methods=['GET'])
def get_model_performance():
    api_impl = model_perf_impl.get_model_performance
    return get_data(request.path, api_impl)

""" 
Returns all historical and predicted prices for a specific stock (Feature 2)
Return dict where key = date in epoch and value = price in USD
"""
@app.route('/stock/<ticker>/prices', methods=['GET'])
def get_stock_prices(ticker):
    api_impl = stock_prices_impl.get_stock_prices
    return get_data(request.path, api_impl, ticker)
    

""" 
Returns all relevant information for a specific stock (Feature 4)
"""
@app.route('/stock/<ticker>/info', methods=['GET'])
def get_stock_info(ticker):
    api_impl = stock_info_impl.fetch_single_stock_data
    return get_data(request.path, api_impl, ticker)

""" 
Returns a list of recent news articles about a specific stock
"""
@app.route('/stock/<ticker>/news', methods=['GET'])
def get_stock_news(ticker):
    api_impl = stock_news_impl.get_stock_news
    return get_data(request.path, api_impl, ticker)

def get_data(request_path, api_impl, *args):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    shelve_path = os.path.join(script_dir, 'cache', 'api_response')
    
    cache_key = f'{request_path}|{str(date.today())}'
    with shelve_lock:
        with shelve.open(shelve_path) as cache:
            data_in_cache = cache_key in cache
            if data_in_cache:
                data = cache[cache_key]
    
    if not data_in_cache:
        data = jsonify(api_impl(*args))
        with shelve_lock:
            with shelve.open(shelve_path) as cache:
                cache[cache_key] = data

    return data

if __name__ == '__main__':
    app.run(debug=True)
