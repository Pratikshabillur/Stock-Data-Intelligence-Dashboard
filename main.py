from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from predictor import predict_next_7_days
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

from data_collector import fetch_stock, STOCKS

app = FastAPI(title="Stock Dashboard API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ─── In-memory cache ─────────────────────────────────────
_cache = {}
CACHE_TTL_MINUTES = 10

def get_cached(key: str):
    """Return cached value if not expired."""
    if key in _cache:
        data, timestamp = _cache[key]
        if datetime.now() - timestamp < timedelta(minutes=CACHE_TTL_MINUTES):
            print(f"[CACHE HIT] {key}")
            return data
    print(f"[CACHE MISS] {key}")
    return None

def set_cache(key: str, value):
    """Store value in cache with timestamp."""
    _cache[key] = (value, datetime.now())


# ─── Helper: fetch with caching + error handling ─────────
def get_df(symbol: str, period: str = "1y") -> pd.DataFrame:
    symbol = symbol.upper()
    if symbol not in STOCKS:
        raise HTTPException(
            status_code=404,
            detail=f"{symbol} not found. Use /companies to see valid symbols."
        )
    cache_key = f"{symbol}_{period}"
    cached = get_cached(cache_key)
    if cached is not None:
        return cached
    df = fetch_stock(symbol, STOCKS[symbol], period=period)
    set_cache(cache_key, df)
    return df


# ─── 1. GET /companies ───────────────────────────────────
@app.get("/companies")
def get_companies():
    """Returns list of all available stock symbols."""
    return {"companies": list(STOCKS.keys())}


# ─── 2. GET /data/{symbol} ───────────────────────────────
@app.get("/data/{symbol}")
def get_stock_data(symbol: str):
    """Returns last 30 days of stock data with all metrics."""
    df = get_df(symbol, period="3mo")
    df = df.tail(30).copy()
    df["Date"] = df["Date"].astype(str)
    return {
        "symbol": symbol.upper(),
        "data": df.to_dict(orient="records")
    }


# ─── 3. GET /summary/{symbol} ────────────────────────────
@app.get("/summary/{symbol}")
def get_summary(symbol: str):
    """Returns 52-week high, low, average close and volatility."""
    df = get_df(symbol)
    latest = df.iloc[-1]
    return {
        "symbol":        symbol.upper(),
        "52_week_high":  round(float(df["52w_High"].iloc[-1]), 2),
        "52_week_low":   round(float(df["52w_Low"].iloc[-1]), 2),
        "avg_close":     round(float(df["Close"].mean()), 2),
        "latest_price":  round(float(latest["Close"]), 2),
        "daily_return":  round(float(latest["Daily_Return"]), 2),
        "volatility":    round(float(latest["Volatility"]), 2)
    }


# ─── 4. GET /compare ─────────────────────────────────────
@app.get("/compare")
def compare_stocks(
    symbol1: str = Query(..., description="First stock e.g. TCS"),
    symbol2: str = Query(..., description="Second stock e.g. INFY")
):
    """Compare two stocks: closing prices and daily returns side by side."""
    df1 = get_df(symbol1).tail(30)[["Date", "Close", "Daily_Return"]].copy()
    df2 = get_df(symbol2).tail(30)[["Date", "Close", "Daily_Return"]].copy()
    df1["Date"] = df1["Date"].astype(str)
    df2["Date"] = df2["Date"].astype(str)
    s1, s2 = symbol1.upper(), symbol2.upper()
    return {
        "symbol1": s1,
        "symbol2": s2,
        "data": {
            s1: df1.to_dict(orient="records"),
            s2: df2.to_dict(orient="records")
        },
        "summary": {
            s1: {
                "avg_close":        round(float(df1["Close"].mean()), 2),
                "avg_daily_return": round(float(df1["Daily_Return"].mean()), 4)
            },
            s2: {
                "avg_close":        round(float(df2["Close"].mean()), 2),
                "avg_daily_return": round(float(df2["Daily_Return"].mean()), 4)
            }
        }
    }


@app.get("/gainers")
def top_gainers_losers():
    """Returns today's top gainers and losers across all stocks."""
    results = []

    for symbol, ticker in STOCKS.items():
        try:
            cache_key = f"{symbol}_5d"
            cached = get_cached(cache_key)

            if cached is not None:
                df = cached
            else:
                df = fetch_stock(symbol, ticker, period="5d")
                set_cache(cache_key, df)

            # ✅ Skip invalid data
            if df is None or df.empty or "Close" not in df.columns:
                continue

            # ✅ Ensure enough rows
            if len(df) < 2:
                continue

            latest = df.iloc[-1]

            results.append({
                "symbol": symbol,
                "latest_price": round(float(latest.get("Close", 0)), 2),
                "daily_return": round(float(latest.get("Daily_Return", 0)), 2)
            })

        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")
            continue

    # ✅ Handle no data case
    if not results:
        raise HTTPException(status_code=500, detail="No stock data available")

    # Sort by daily return
    results.sort(key=lambda x: x["daily_return"], reverse=True)

    return {
        "top_gainers": results[:3],
        "top_losers": results[-3:][::-1]
    }

# ─── 6. GET /predict/{symbol} ────────────────────────────
@app.get("/predict/{symbol}")
def predict_price(symbol: str):
    """Predicts next 7 days of closing price using Linear Regression."""
    result = predict_next_7_days(symbol.upper())
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Could not generate prediction for {symbol}"
        )
    return result


# ─── 7. GET /cache/status ────────────────────────────────
@app.get("/cache/status")
def cache_status():
    """Shows what is currently cached and when it expires."""
    status = {}
    for key, (_, timestamp) in _cache.items():
        expires_in = CACHE_TTL_MINUTES - (datetime.now() - timestamp).seconds // 60
        status[key] = {
            "cached_at":  timestamp.strftime("%H:%M:%S"),
            "expires_in": f"{max(0, expires_in)} min"
        }
    return {"cached_keys": len(_cache), "entries": status}
