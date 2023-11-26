from flask import Flask, jsonify
from flask_cors import CORS
from api_impl import stock_info_impl, tickers_impl, stock_prices_impl, stock_news_impl, model_perf_impl

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})


'''
Returns a list of all tickers we are tracking (Feature 1)
'''
@app.route('/tickers', methods=['GET'])
def get_stock_tickers():
    stock_tickers = tickers_impl.get_stock_tickers()
    response = jsonify(stock_tickers)
    return response


'''
Returns the model's performance information
'''
@app.route('/model/performance', methods=['GET'])
def get_model_performance():
    model_performance = model_perf_impl.get_model_performance()
    response = jsonify(model_performance)
    return response

""" 
Returns all historical and predicted prices for a specific stock (Feature 2)
Return dict where key = date in epoch and value = price in USD
"""
@app.route('/stock/<ticker>/prices', methods=['GET'])
def get_stock_prices(ticker):
    stock_prices = stock_prices_impl.get_stock_prices(ticker)
    response = jsonify(stock_prices)
    return response

""" 
Returns all relevant information for a specific stock (Feature 4)
"""
@app.route('/stock/<ticker>/info', methods=['GET'])
def get_stock_info(ticker):
    stock_info = stock_info_impl.fetch_single_stock_data(ticker)
    response = jsonify(stock_info)
    return response

""" 
Returns a list of recent news articles about a specific stock
"""
@app.route('/stock/<ticker>/news', methods=['GET'])
def get_stock_news(ticker):
    stock_news = stock_news_impl.get_stock_news(ticker)
    response = jsonify(stock_news)
    return response

if __name__ == '__main__':
    app.run(debug=True)
