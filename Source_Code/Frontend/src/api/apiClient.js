const API_BASE = 'http://localhost:5219/api';

async function fetchApi(endpoint, options = {}) {
  try {
    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });
    if (!response.ok) throw new Error(`API Error: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.warn(`API call failed for ${endpoint}:`, error.message);
    return null;
  }
}

export const api = {
  getDashboardSummary: () => fetchApi('/dashboard/summary'),
  
  getLatestCandle: (symbol = 'BTCUSDT', exchange = 'Binance', interval = 'OneMinute') =>
    fetchApi(`/market/latest?exchange=${exchange}&symbol=${symbol}&interval=${interval}`),
  
  getCandles: (symbol = 'BTCUSDT', exchange = 'Binance', interval = 'OneMinute', from, to) =>
    fetchApi(`/market/candles?exchange=${exchange}&symbol=${symbol}&interval=${interval}&from=${from}&to=${to}`),
    
  getLatestPrediction: (symbol = 'BTCUSDT') =>
    fetchApi(`/predictions/latest?symbol=${symbol}`),
    
  getPredictionHistory: (symbol = 'BTCUSDT', from, to) =>
    fetchApi(`/predictions/history?symbol=${symbol}&from=${from}&to=${to}`),
    
  getFeatures: (symbol = 'BTCUSDT', interval = 'OneMinute', from, to) =>
    fetchApi(`/features?symbol=${symbol}&interval=${interval}&from=${from}&to=${to}`),
    
  getRegimeCurrent: (symbol = 'BTCUSDT') =>
    fetchApi(`/regime/current?symbol=${symbol}`),
    
  getModelRegistry: () => fetchApi('/models/registry'),

  getModelMetrics: (modelName) => fetchApi(`/models/metrics?modelName=${modelName}`),

  getSimilarPatterns: (symbol = 'BTCUSDT', limit = 5) =>
    fetchApi(`/patterns/similar?symbol=${symbol}&limit=${limit}`),

  getHealth: () => fetchApi('/health'),
};

