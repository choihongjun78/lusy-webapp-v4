
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/api/simulate")
def simulate(symbol: str = Query(...), monthly: str = Query(...), years: str = Query(...)):
    try:
        monthly = int(monthly)
        years = int(years)

        end = datetime.today()
        start = end - timedelta(days=365 * years)
        data = yf.download(symbol, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), interval='1mo')

        close_prices = data['Close'].dropna().tolist()

        total_cost = 0
        total_unit = 0
        for price in close_prices:
            price = float(price)
            total_cost += monthly
            total_unit += monthly / price

        final_value = total_unit * float(close_prices[-1])
        result = {
            "symbol": symbol,
            "invested": total_cost,
            "value": round(final_value),
            "return_percent": round((final_value - total_cost) / total_cost * 100, 2)
        }
        return JSONResponse(content=result)

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
