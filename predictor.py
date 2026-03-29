import numpy as np
from sklearn.linear_model import LinearRegression
from data_collector import fetch_stock, STOCKS

def predict_next_7_days(symbol: str):
    """
    Trains a simple Linear Regression on last 60 days of closing prices
    and predicts the next 7 days.
    """
    ticker = STOCKS.get(symbol.upper())
    if not ticker:
        return None

    df = fetch_stock(symbol, ticker, period="3mo")
    if df.empty or len(df) < 30:
        return None

    # Use last 60 days
    df = df.tail(60).copy()
    closes = df["Close"].values

    # X = day number (0,1,2...), Y = closing price
    X = np.arange(len(closes)).reshape(-1, 1)
    y = closes

    # Train the model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next 7 days
    future_X = np.arange(len(closes), len(closes) + 7).reshape(-1, 1)
    predictions = model.predict(future_X)

    # Last 10 actual days for chart context
    last_dates  = df["Date"].astype(str).tolist()[-10:]
    last_prices = [round(float(p), 2) for p in closes[-10:]]

    return {
        "symbol": symbol.upper(),
        "last_10_actual": {
            "dates":  last_dates,
            "prices": last_prices
        },
        "predicted_7_days": {
            "prices": [round(float(p), 2) for p in predictions],
            "note": "Linear regression on last 60 days — indicative only"
        },
        "model_info": {
            "type": "LinearRegression",
            "trained_on": f"{len(closes)} days of data",
            "slope": round(float(model.coef_[0]), 4),
            "direction": "upward" if model.coef_[0] > 0 else "downward"
        }
    }