
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import yfinance as yf
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/api/simulate")
def simulate(symbol: str = Query(...), monthly: str = Query(...), years: str = Query(...)):
    try:
        # 강제 정수 변환
        monthly = int(monthly)
        years = int(years)

        # 데이터 수집
        end = datetime.today()
        start = end - timedelta(days=365 * years)
        data = yf.download(tickers=symbol, start=start, end=end, interval='1mo')

        # 오류 방지: 'Close' 컬럼 존재 여부 확인
        if 'Close' not in data.columns:
            return JSONResponse(status_code=500, content={"error": "No 'Close' price data available for this symbol."})

        # 종가 시리즈 추출
        close_series = data['Close']

        # 오류 방지: Series 내 각 항목이 유효한 수치인지 확인 후 변환
        close_prices = []
        for p in close_series.dropna():
            try:
                close_prices.append(float(p))
            except ValueError:
                return JSONResponse(status_code=500, content={"error": f"Invalid price found: {p}"})

        # 적립식 투자 시뮬레이션
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
