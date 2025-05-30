
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/api/simulate")
def simulate(symbol: str = Query(...), monthly: str = Query(...), years: str = Query(...)):
    try:
        monthly = int(monthly)
        years = int(years)

        end = datetime.today()
        start = end - timedelta(days=365 * years)
        data = yf.download(tickers=symbol, start=start, end=end, interval='1mo')

        if 'Close' not in data.columns:
            return JSONResponse(status_code=500, content={"error": "No 'Close' price data available for this symbol."})

        close_series = data['Close']
        if isinstance(close_series, pd.DataFrame):
            close_series = close_series[symbol.upper()]

        close_prices = [float(p) for p in close_series.dropna()]

        total_cost = 0
        total_unit = 0
        for price in close_prices:
            total_cost += monthly
            total_unit += monthly / price

        final_value = total_unit * close_prices[-1]
        result = {
            "symbol": symbol.upper(),
            "invested": total_cost,
            "value": round(final_value),
            "return_percent": round((final_value - total_cost) / total_cost * 100, 2)
        }
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
