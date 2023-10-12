# CSI4900-Stock-Prediction-Project

## Overview

This web application offers two primary functionalities:

1. Fetches various financial indicators for a list of stock tickers.
2. Retrieves key metrics like market cap, sector, dividend yield, etc., for the same stock tickers.

The data is fetched and calculated by REST API endpoints and is accessible via HTTP GET requests.

## Table of Contents

- [Getting Started](#getting-started)
- [Dependencies](#dependencies)
- [How to Run](#how-to-run)
- [API Endpoints](#api-endpoints)
- [Contributors](#contributors)

## Getting Started

Clone the repository to your local machine.

```
git clone https://github.com/your_repository/CSI4900-Stock-Prediction-Project.git
```

Navigate to the project directory.

```
cd CSI4900-Stock-Prediction-Project
```

## Dependencies

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
python main.py
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
- `main.py`: Defines the Flask app and API endpoints.

## Contributors

- CSI4900 Students
