<<<<<<< HEAD
import yfinance as yf
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# Real NSE Indian stock symbols
STOCKS = {
    "TCS": "TCS.NS",
    "INFY": "INFY.NS",
    "RELIANCE": "RELIANCE.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "WIPRO": "WIPRO.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "SBIN": "SBIN.NS"
}

def fetch_stock(symbol: str, ticker: str, period: str = "1y"):
    """Fetch, clean, and enrich stock data with required metrics."""
    print(f"Fetching data for {symbol} ({ticker})...")

    df = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

    # ✅ Fix MultiIndex issue (VERY IMPORTANT)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if df.empty:
        print(f"⚠️ No data received for {symbol}")
        return pd.DataFrame()

    # Reset index → Date becomes column
    df = df.reset_index()

    # Convert Date format
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    # Sort data
    df = df.sort_values('Date').reset_index(drop=True)

    # Drop missing values
    df = df.dropna()

    # === Metrics ===
    df["Daily_Return"] = (df["Close"] - df["Open"]) / df["Open"] * 100
    df["MA_7"] = df["Close"].rolling(window=7, min_periods=1).mean()
    df["Volatility"] = df["Daily_Return"].rolling(window=30, min_periods=1).std()

    # ✅ Correct 52-week High/Low
    df["52w_High"] = df["High"].rolling(window=252, min_periods=1).max()
    df["52w_Low"] = df["Low"].rolling(window=252, min_periods=1).min()

    df["Symbol"] = symbol

    # Keep clean columns
    df = df[[
        "Date", "Open", "High", "Low", "Close", "Volume",
        "Daily_Return", "MA_7", "52w_High", "52w_Low",
        "Volatility", "Symbol"
    ]]

    return df


# ====================== TEST / RUN ======================
# ====================== TEST / RUN ======================
if __name__ == "__main__":
    all_data = {}

    for symbol, ticker in STOCKS.items():
        df = fetch_stock(symbol, ticker)
        if not df.empty:
            all_data[symbol] = df
            print(f"✅ {symbol}: {len(df)} rows fetched")

    # === Show TCS last 5 days ===
    print("\n=== TCS Last 5 Days ===")
    if "TCS" in all_data:
        print(
            all_data["TCS"][["Date", "Close", "Daily_Return", "MA_7", "Volatility"]]
            .tail()
            .to_string(index=False)
        )

    # === Show 52-week High/Low ===
    print("\n=== 52-Week High/Low for each stock ===")
    for symbol, df in all_data.items():
        high = float(df["52w_High"].iloc[-1])
        low  = float(df["52w_Low"].iloc[-1])
        latest = float(df["Close"].iloc[-1])
        print(f"{symbol:10} | High: ₹{high:8.2f} | Low: ₹{low:8.2f} | Latest: ₹{latest:8.2f}")

    # === Correlation: TCS vs INFY ===   ← must be INSIDE this block
    print("\n=== Correlation: TCS vs INFY (last 1 year) ===")
    tcs_returns  = all_data["TCS"]["Daily_Return"]
    infy_returns = all_data["INFY"]["Daily_Return"]
    corr = round(float(tcs_returns.corr(infy_returns)), 4)
    print(f"Correlation coefficient: {corr}")
    if corr > 0.7:
        print("→ Strong positive correlation (they move together)")
    elif corr > 0.4:
        print("→ Moderate correlation")
    else:
        print("→ Weak correlation")
=======
import yfinance as yf
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# Real NSE Indian stock symbols
STOCKS = {
    "TCS": "TCS.NS",
    "INFY": "INFY.NS",
    "RELIANCE": "RELIANCE.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "WIPRO": "WIPRO.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "SBIN": "SBIN.NS"
}

def fetch_stock(symbol: str, ticker: str, period: str = "1y"):
    """Fetch, clean, and enrich stock data with required metrics."""
    print(f"Fetching data for {symbol} ({ticker})...")

    df = yf.download(
        ticker,
        period=period,
        auto_adjust=True,
        progress=False
    )

    # ✅ Fix MultiIndex issue (VERY IMPORTANT)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    if df.empty:
        print(f"⚠️ No data received for {symbol}")
        return pd.DataFrame()

    # Reset index → Date becomes column
    df = df.reset_index()

    # Convert Date format
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    # Sort data
    df = df.sort_values('Date').reset_index(drop=True)

    # Drop missing values
    df = df.dropna()

    # === Metrics ===
    df["Daily_Return"] = (df["Close"] - df["Open"]) / df["Open"] * 100
    df["MA_7"] = df["Close"].rolling(window=7, min_periods=1).mean()
    df["Volatility"] = df["Daily_Return"].rolling(window=30, min_periods=1).std()

    # ✅ Correct 52-week High/Low
    df["52w_High"] = df["High"].rolling(window=252, min_periods=1).max()
    df["52w_Low"] = df["Low"].rolling(window=252, min_periods=1).min()

    df["Symbol"] = symbol

    # Keep clean columns
    df = df[[
        "Date", "Open", "High", "Low", "Close", "Volume",
        "Daily_Return", "MA_7", "52w_High", "52w_Low",
        "Volatility", "Symbol"
    ]]

    return df


# ====================== TEST / RUN ======================
# ====================== TEST / RUN ======================
if __name__ == "__main__":
    all_data = {}

    for symbol, ticker in STOCKS.items():
        df = fetch_stock(symbol, ticker)
        if not df.empty:
            all_data[symbol] = df
            print(f"✅ {symbol}: {len(df)} rows fetched")

    # === Show TCS last 5 days ===
    print("\n=== TCS Last 5 Days ===")
    if "TCS" in all_data:
        print(
            all_data["TCS"][["Date", "Close", "Daily_Return", "MA_7", "Volatility"]]
            .tail()
            .to_string(index=False)
        )

    # === Show 52-week High/Low ===
    print("\n=== 52-Week High/Low for each stock ===")
    for symbol, df in all_data.items():
        high = float(df["52w_High"].iloc[-1])
        low  = float(df["52w_Low"].iloc[-1])
        latest = float(df["Close"].iloc[-1])
        print(f"{symbol:10} | High: ₹{high:8.2f} | Low: ₹{low:8.2f} | Latest: ₹{latest:8.2f}")

    # === Correlation: TCS vs INFY ===   ← must be INSIDE this block
    print("\n=== Correlation: TCS vs INFY (last 1 year) ===")
    tcs_returns  = all_data["TCS"]["Daily_Return"]
    infy_returns = all_data["INFY"]["Daily_Return"]
    corr = round(float(tcs_returns.corr(infy_returns)), 4)
    print(f"Correlation coefficient: {corr}")
    if corr > 0.7:
        print("→ Strong positive correlation (they move together)")
    elif corr > 0.4:
        print("→ Moderate correlation")
    else:
        print("→ Weak correlation")
>>>>>>> fb497c35f163bbdc55299408e1397899674d5c50
