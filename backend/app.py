from flask import Flask, jsonify
from flask_cors import CORS
from api_impl import stock_info_impl, tickers_impl

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/tickers', methods=['GET'])
def get_stock_tickers():
    '''
    Returns a list of all tickers we are tracking
    '''
    stock_tickers = tickers_impl.get_stock_tickers()
    response = jsonify(stock_tickers)
    return response

@app.route('/stock/<ticker>/info', methods=['GET'])
def get_stock_info(ticker):
    """ 
    Returns all relevant information for a specific stock
    """
    stock_info = stock_info_impl.fetch_single_stock_data(ticker)
    response = jsonify(stock_info)
    return response

if __name__ == '__main__':
    app.run(debug=True)
