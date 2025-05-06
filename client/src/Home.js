import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  LineChart,
  Line,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

function Home() {
  const [spendings, setSpendings] = useState([]);
  const [frame, setFrame] = useState('daily');
  const [range, setRange] = useState(1);
  const [currency, setCurrency] = useState('CAD');
  const [currencies, setCurrencies] = useState([]);

  // Fetch supported currencies
  useEffect(() => {
    axios.get('/api/currencies')
      .then(res => {
        setCurrencies(res.data);
        const defaultCurrency = res.data.find(c => c.default)?.currency || 'CAD';
        setCurrency(defaultCurrency);
      });
  }, []);

  // Fetch spending data when filters change
  useEffect(() => {
    axios.get(`/api/spendings?frame=${frame}&range=${range}&currency=${currency}`)
      .then(res => setSpendings(res.data.spendings))
      .catch(err => console.error(err));
  }, [frame, range, currency]);

  return (
    <div style={{ padding: 20 }}>
      <h1>Welcome to My Spending App</h1>
      
      {/* Filter Controls - Ordered as frame -> range -> currency */}
      <div style={{ marginBottom: 20, display: 'flex', gap: 10 }}>
        <select value={frame} onChange={(e) => setFrame(e.target.value)}>
          <option value="daily">Daily</option>
          <option value="monthly">Monthly</option>
          <option value="yearly">Yearly</option>
        </select>

        <select value={range} onChange={(e) => setRange(e.target.value)}>
          {[1, 2, 3, 4, 5, 6].map(num => (
            <option key={num} value={num}>Last {num} {frame}</option>
          ))}
        </select>

        <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
          {currencies.map(curr => (
            <option key={curr.currency} value={curr.currency}>
              {curr.currency} ({curr.symbol})
            </option>
          ))}
        </select>
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={spendings}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="startDate" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="totalAmount" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export default Home;