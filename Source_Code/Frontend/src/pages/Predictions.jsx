import React from 'react';
import { GlassCard } from '../components/GlassCard';
import { ProbabilityBar } from '../components/ProbabilityBar';
import { recentPredictions } from '../data/mockData';
import { api } from '../api/apiClient';
import { useApi } from '../hooks/useApi';
import { Wifi, WifiOff } from 'lucide-react';

const DIRECTION_MAP = { 0: 'DOWN', 1: 'NEUTRAL', 2: 'UP' };

const Predictions = () => {
  const { data: latestPrediction } = useApi(() => api.getLatestPrediction('BTCUSDT'), [], 15000);

  const isLive = latestPrediction !== null;

  const direction = latestPrediction ? (DIRECTION_MAP[latestPrediction.direction] || 'UP') : 'UP';
  const confidence = latestPrediction ? (latestPrediction.confidence * 100).toFixed(0) : 87;
  const upProb = latestPrediction ? (latestPrediction.upProbability * 100).toFixed(0) : 87;
  const downProb = latestPrediction ? (latestPrediction.downProbability * 100).toFixed(0) : 4;
  const neutralProb = latestPrediction ? (latestPrediction.neutralProbability * 100).toFixed(0) : 9;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <h1 className="page-title" style={{ marginBottom: 0 }}>Live Predictions</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', opacity: 0.6 }}>
          {isLive ? <Wifi size={14} color="var(--accent-green)" /> : <WifiOff size={14} color="var(--accent-amber)" />}
          <span>{isLive ? 'Live Data' : 'Mock Data'}</span>
        </div>
      </div>

      <div className="grid grid-cols-3" style={{ marginBottom: '24px' }}>
        <GlassCard>
          <div style={{ textAlign: 'center', marginBottom: '24px' }}>
            <h3 style={{ color: 'var(--text-secondary)' }}>BTC/USD Next 1H</h3>
            <div style={{ 
              fontSize: '48px', fontWeight: 'bold', margin: '16px 0',
              color: direction === 'UP' ? 'var(--accent-green)' : direction === 'DOWN' ? 'var(--accent-red)' : 'var(--accent-amber)'
            }}>
              {direction}
            </div>
            <div style={{ fontSize: '24px', fontWeight: '600' }}>{confidence}% Confidence</div>
          </div>
          <ProbabilityBar probability={upProb} label="Bullish" color="var(--accent-green)" />
          <ProbabilityBar probability={neutralProb} label="Neutral" color="var(--accent-amber)" />
          <ProbabilityBar probability={downProb} label="Bearish" color="var(--accent-red)" />
        </GlassCard>

        <GlassCard style={{ gridColumn: 'span 2' }}>
           <div style={{ marginBottom: '16px', fontWeight: '600' }}>Prediction History</div>
           <table className="data-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Asset</th>
                <th>Predicted</th>
                <th>Confidence</th>
                <th>Result</th>
              </tr>
            </thead>
            <tbody>
              {recentPredictions.map(pred => (
                <tr key={pred.id}>
                  <td>{pred.time}</td>
                  <td>{pred.pair}</td>
                  <td className={pred.direction === 'UP' ? 'text-green' : 'text-red'} style={{ fontWeight: 'bold' }}>
                    {pred.direction}
                  </td>
                  <td>{pred.confidence}%</td>
                  <td>
                    <span className={`badge ${pred.outcome === 'SUCCESS' ? 'badge-green' : pred.outcome === 'FAILED' ? 'badge-red' : 'badge-amber'}`}>
                      {pred.outcome}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </GlassCard>
      </div>
    </div>
  );
};

export default Predictions;
