import { useState } from "react";

export default function Home() {
  const [symbol, setSymbol] = useState("SCHD");
  const [monthlyInvestment, setMonthlyInvestment] = useState(500000);
  const [investmentYears, setInvestmentYears] = useState(12);
  const [result, setResult] = useState(null);

  const runSimulation = async () => {
    const res = await fetch(`/api/simulate?symbol=${symbol}&monthly=${monthlyInvestment}&years=${investmentYears}`);
    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial, sans-serif" }}>
      <h1>LUSY 투자 시뮬레이터</h1>
      <div style={{ marginBottom: "20px" }}>
        <label>티커 (예: SCHD): </label>
        <input value={symbol} onChange={e => setSymbol(e.target.value)} />
      </div>
      <div style={{ marginBottom: "20px" }}>
        <label>월 적립금 (₩): </label>
        <input type="number" value={monthlyInvestment} onChange={e => setMonthlyInvestment(Number(e.target.value))} />
      </div>
      <div style={{ marginBottom: "20px" }}>
        <label>투자 기간 (년): </label>
        <input type="number" value={investmentYears} onChange={e => setInvestmentYears(Number(e.target.value))} />
      </div>
      <button onClick={runSimulation}>시뮬레이션 실행</button>

      {result && (
        <div style={{ marginTop: "40px" }}>
          <h2>결과</h2>
          <p><strong>종목:</strong> {result.symbol}</p>
          <p><strong>총 투자금:</strong> ₩{result.invested.toLocaleString()}</p>
          <p><strong>최종 평가금액:</strong> ₩{result.value.toLocaleString()}</p>
          <p><strong>수익률:</strong> {result.return_percent}%</p>
        </div>
      )}
    </div>
  );
}
