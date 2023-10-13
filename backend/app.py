from flask import Flask, jsonify
from flask_cors import CORS
from financial_calculations import calculate_indicators, fetch_stock_data

app = Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

# http://<server_address>:<port>/get_indicators, 
@app.route('/get_indicators', methods=['GET'])
def get_indicators():
    # This function returns a DataFrame containing various financial indicators.
    indicators_df = calculate_indicators()
    
    indicators_json = indicators_df.to_json(orient='split')
    response = jsonify(indicators_json)
    
    return response

# http://<server_address>:<port>/get_stock_data, 
@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    # This function returns a dictionary containing various data points for different stocks.
    stock_data = fetch_stock_data()
    
    response = jsonify(stock_data)
    
    return response

if __name__ == '__main__':
    app.run(debug=True)
