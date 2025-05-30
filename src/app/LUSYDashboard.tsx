
import React, { useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

export default function LUSYDashboard() {
  const [monthlyInvestment, setMonthlyInvestment] = useState(500000);
  const [investmentYears, setInvestmentYears] = useState(12);
  const [data, setData] = useState([]);
  const [symbol, setSymbol] = useState('SCHD');

  const simulateInvestment = async () => {
    const res = await fetch(`https://lusy-api.vercel.app/api/simulate?symbol=${symbol}&monthly=${monthlyInvestment}&years=${investmentYears}`);
    const result = await res.json();
    setData(result);
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>LUSY 투자 시뮬레이터</h2>
      <input value={symbol} onChange={e => setSymbol(e.target.value.toUpperCase())} placeholder="ETF 티커 (예: SCHD)" />
      <input type="number" value={monthlyInvestment} onChange={e => setMonthlyInvestment(Number(e.target.value))} placeholder="월 투자금" />
      <input type="number" value={investmentYears} onChange={e => setInvestmentYears(Number(e.target.value))} placeholder="투자 기간 (년)" />
      <button onClick={simulateInvestment}>시뮬레이션 실행</button>

      {data.length > 0 && (
        <LineChart width={800} height={400} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="Date" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Total Invested" stroke="#8884d8" />
          <Line type="monotone" dataKey="Net Value" stroke="#82ca9d" />
        </LineChart>
      )}
    </div>
  );
}
