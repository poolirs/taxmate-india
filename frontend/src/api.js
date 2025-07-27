export async function fetchTaxCalculation(income) {
  const response = await fetch('http://127.0.0.1:8000/calculate-tax', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ income })
  });
  if (!response.ok) throw new Error('Error calculating tax');
  return response.json();
}
