# CSI4900-Stock-Prediction-Project

Certainly! Here's a README.md file content that provides an overview and instructions for your Flask application and its associated financial calculations.

---

# Financial Indicators API with Flask

## Overview

This project is a RESTful API developed with Flask to calculate various financial indicators for the top 10 S&P 500 companies. It fetches historical stock data and computes a set of financial indicators such as Simple Moving Average (SMA), Exponential Moving Average (EMA), Bollinger Bands, Relative Strength Index (RSI), and Moving Average Convergence Divergence (MACD).

## Features

- RESTful API endpoint to fetch computed financial indicators.
- Data fetching from Yahoo Finance using the `yfinance` package.
- Data manipulation and statistical calculations using `pandas` and `numpy`.

## Requirements

- Python 3.x
- Flask
- yfinance
- pandas
- numpy

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your_username/CSI4900-Stock-Prediction-Project.git
    ```

2. Navigate to the project directory:
    ```bash
    cd CSI4900-Stock-Prediction-Project
    ```

3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Flask application:
    ```bash
    python main.py
    ```

2. To fetch financial indicators, use your web browser or a tool like curl to visit:
    ```http
    http://localhost:5000/get_indicators
    ```

## API Documentation

### GET `/get_indicators`

Returns a JSON object containing various calculated financial indicators for the top 10 S&P 500 companies.

#### Response

- JSON object with the calculated indicators.

## Code Structure

- `main.py`: Contains the Flask API endpoints.
- `financial_calculations.py`: Contains the function for calculating the financial indicators.
