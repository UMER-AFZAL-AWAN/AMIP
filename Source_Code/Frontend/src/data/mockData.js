// Realistic mock data for a trading dashboard

const generateCandles = (count, startPrice) => {
  const data = [];
  let currentPrice = startPrice;
  let time = Date.now() - count * 3600000; // hourly
  for (let i = 0; i < count; i++) {
    const volatility = currentPrice * 0.005;
    const open = currentPrice;
    const high = open + Math.random() * volatility;
    const low = open - Math.random() * volatility;
    const close = low + Math.random() * (high - low);
    const volume = Math.floor(Math.random() * 5000) + 1000;
    
    data.push({
      time: new Date(time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
      open, high, low, close, volume,
      price: close, // simplified for sparklines
    });
    currentPrice = close;
    time += 3600000;
  }
  return data;
};

export const btcData = generateCandles(100, 66500);

export const recentPredictions = [
  { id: 1, time: '10 mins ago', pair: 'BTC/USD', direction: 'UP', confidence: 87, outcome: 'PENDING' },
  { id: 2, time: '1 hour ago', pair: 'ETH/USD', direction: 'DOWN', confidence: 65, outcome: 'SUCCESS' },
  { id: 3, time: '3 hours ago', pair: 'SOL/USD', direction: 'UP', confidence: 92, outcome: 'SUCCESS' },
  { id: 4, time: '4 hours ago', pair: 'BTC/USD', direction: 'UP', confidence: 78, outcome: 'FAILED' },
  { id: 5, time: '8 hours ago', pair: 'AVAX/USD', direction: 'DOWN', confidence: 81, outcome: 'SUCCESS' },
];

export const models = [
  { id: 'm-1', name: 'Alpha-X Gradient', version: 'v2.4.1', status: 'ACTIVE', accuracy: 68.4, deployed: '2026-07-15' },
  { id: 'm-2', name: 'LSTM Volatility', version: 'v1.9.0', status: 'ACTIVE', accuracy: 62.1, deployed: '2026-06-22' },
  { id: 'm-3', name: 'Transformer-Regime', version: 'v3.0.beta', status: 'TRAINING', accuracy: 71.2, deployed: 'N/A' },
  { id: 'm-4', name: 'Sentiment-BERT', version: 'v1.2', status: 'INACTIVE', accuracy: 54.8, deployed: '2026-01-10' },
];

export const patterns = [
  { id: 'p-1', name: 'Wyckoff Accumulation', asset: 'BTC', similarity: 94, timeframe: '4H', expectedOutcome: 'BULLISH' },
  { id: 'p-2', name: 'Head & Shoulders', asset: 'ETH', similarity: 88, timeframe: '1H', expectedOutcome: 'BEARISH' },
  { id: 'p-3', name: 'Ascending Triangle', asset: 'SOL', similarity: 91, timeframe: '15m', expectedOutcome: 'BULLISH' },
];
