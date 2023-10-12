from flask import Flask, jsonify, json
from financial_calculations import calculate_indicators  # Import the function

app = Flask(__name__)

@app.route('/get_indicators', methods=['GET'])
def get_indicators():
    indicators_df = calculate_indicators()  # Call the function to get indicators DataFrame
    
    indicators_json = indicators_df.to_json(orient='split')
    
    # Convert to a Flask Response object
    response = jsonify(indicators_json)

    return response
