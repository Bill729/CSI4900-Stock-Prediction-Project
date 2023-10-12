# Import necessary modules from Flask library and your own financial_calculations script
from flask import Flask, jsonify, json
from financial_calculations import calculate_indicators, fetch_stock_data

# Create a new Flask web application. '__name__' is a special variable 
# that gets the Python script’s name when the script is executed.
app = Flask(__name__)

# Define a URL route for fetching financial indicators. 
# When you visit http://<server_address>:<port>/get_indicators, 
# this function will be executed.
@app.route('/get_indicators', methods=['GET'])
def get_indicators():

    # Call the 'calculate_indicators' function from your financial_calculations script.
    # This function returns a DataFrame containing various financial indicators.
    indicators_df = calculate_indicators()
    
    # Convert the DataFrame to JSON format. 
    # 'orient="split"' specifies how the data should be oriented in the JSON output.
    indicators_json = indicators_df.to_json(orient='split')
    
    # Convert the JSON data into a Flask Response object so it can be sent to the front-end.
    response = jsonify(indicators_json)
    
    # Return the Flask Response object.
    return response

# Define another URL route for fetching general stock data.
# When you visit http://<server_address>:<port>/get_stock_data, 
# this function will be executed.
@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    # Call the 'fetch_stock_data' function from your financial_calculations script.
    # This function returns a dictionary containing various data points for different stocks.
    stock_data = fetch_stock_data()
    
    # Convert the dictionary into a Flask Response object so it can be sent to the front-end.
    response = jsonify(stock_data)
    
    # Return the Flask Response object.
    return response

# This block is a standard piece of code in Flask.
# It means: only run the application if this script is executed directly 
# (not imported as a module in another script).
if __name__ == '__main__':
    # Run the Flask application.
    # The 'debug=True' allows for debugging capabilities.
    app.run(debug=True)
