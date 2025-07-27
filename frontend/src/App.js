import React, { useState } from 'react';
import './App.css';
import { fetchTaxCalculation } from './api';

function App() {
  const [income, setIncome] = useState('');
  const [tax, setTax] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setTax(null);

    try {
      const data = await fetchTaxCalculation(Number(income));
      setTax(data.tax);
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div>
      <h1>Income Tax Calculator</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          value={income}
          onChange={e => setIncome(e.target.value)}
          placeholder="Enter your income"
          required
        />
        <button type="submit">Calculate Tax</button>
      </form>

      {tax !== null && <div>Tax: {tax}</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
    </div>
  );
}

export default App;
