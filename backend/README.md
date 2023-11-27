# Backend Flask APIs

## Dependencies

Supported Python version:

```
Python 3.8.10
```

Before doing any development, using a virtual environment is highly recommended. 
Create a virtual environment:

```
python3 -m venv env
```

Activate your virtual environment:

```
.\env\Scripts\activate
```

Deactivate the virtual environment:

```
deactivate
```

To install the required packages, run:

```
pip install -r requirements.txt
```

The key libraries used are:

- Flask: for the web application.
- Pandas: for data manipulation.
- yfinance: for fetching stock data.
- concurrent.futures: for parallel execution.

## How to Run

Start the Flask development server by running:

```
python app.py
```

Now the app should be running at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. Get Financial Indicators

Fetch various financial indicators like SMA, EMA, RSI, etc., for different stocks.

- **URL:** `/get_indicators`
- **Method:** `GET`

Example:

```
curl http://127.0.0.1:5000/get_indicators
```

### 2. Get Stock Data

Fetch key metrics like market cap, sector, dividend yield, etc., for different stocks.

- **URL:** `/get_stock_data`
- **Method:** `GET`

Example:

```
curl http://127.0.0.1:5000/get_stock_data
```

## Code Structure

- `financial_calculations.py`: Contains all the logic for fetching and calculating stock data and indicators.
- `app.py`: Defines the Flask app and API endpoints.