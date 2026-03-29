# StockIQ — Stock Data Intelligence Dashboard

A full-stack financial data platform built with FastAPI, Python, and Chart.js.
Fetches real-time NSE stock data, computes analytical metrics, and visualizes
them through an interactive dashboard.

---

## Tech Stack

- **Backend**: Python, FastAPI
- **Data**: yfinance, Pandas, NumPy
- **Frontend**: HTML, CSS, Chart.js
- **Database**: In-memory (yfinance live fetch)

---

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/Pratikshabillur/Stock-Data-Intelligence-Dashboard.git
cd stock_dashboard
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Start the backend server
```bash
uvicorn main:app --reload
```

### 5. Open the dashboard
Open `index.html` in your browser. Make sure uvicorn is running.

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/companies` | GET | List of all tracked NSE stocks |
| `/data/{symbol}` | GET | Last 30 days of OHLCV data + metrics |
| `/summary/{symbol}` | GET | 52-week high, low, avg close, volatility |
| `/compare?symbol1=TCS&symbol2=INFY` | GET | Side-by-side comparison of two stocks |
| `/gainers` | GET | Top 3 gainers and losers of the day |

Full interactive docs available at: `http://localhost:8000/docs`

---

## Metrics Calculated

| Metric | Formula | Purpose |
|---|---|---|
| Daily Return | (Close - Open) / Open × 100 | % move each day |
| 7-Day MA | Rolling 7-day average of Close | Smooths trend noise |
| 52-Week High/Low | Rolling max/min over 252 days | Range context |
| Volatility Score | 30-day std deviation of Daily Return | Risk indicator |
| Correlation | Pearson correlation of two stocks | Co-movement analysis |

---

## Stocks Tracked

TCS · INFY · RELIANCE · HDFCBANK · WIPRO · ICICIBANK · SBIN

---

## Features

- Real NSE stock data via yfinance
- REST API with automatic Swagger documentation
- Interactive price chart with 7-day moving average overlay
- 30D / 14D / 7D time filter
- Top gainers and losers panel
- Live clock and daily return % in sidebar
- Custom volatility score and stock correlation analysis

---
## Optional Add-ons Implemented

- **ML Prediction** — `/predict/{symbol}` uses LinearRegression trained on
  60 days of data to forecast next 7 days of closing price
- **Caching** — All stock data cached for 10 minutes in memory,
  eliminates repeated API calls and speeds up response time
-
- **Deployment** — Live at: https://pratikshabillur.github.io/Stock-Data-Intelligence-Dashboard/

## Project Structure
```
stock_dashboard/
├── main.py             # FastAPI backend — all API endpoints
├── data_collector.py   # Data fetching, cleaning, metric calculation
├── index.html          # Frontend dashboard
├── styles.css          # Dashboard styling
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

*Built as part of Jarnox Internship Assignment — Stock Data Intelligence Dashboard*
