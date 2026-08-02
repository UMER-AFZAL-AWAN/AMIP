import React from 'react';
import { GlassCard } from '../components/GlassCard';
import { ProbabilityBar } from '../components/ProbabilityBar';
import { recentPredictions } from '../data/mockData';

const Predictions = () => {
  return (
    <div>
      <h1 className="page-title">Live Predictions</h1>

      <div className="grid grid-cols-3" style={{ marginBottom: '24px' }}>
        <GlassCard>
          <div style={{ textAlign: 'center', marginBottom: '24px' }}>
            <h3 style={{ color: 'var(--text-secondary)' }}>BTC/USD Next 1H</h3>
            <div style={{ fontSize: '48px', fontWeight: 'bold', color: 'var(--accent-green)', margin: '16px 0' }}>UP</div>
            <div style={{ fontSize: '24px', fontWeight: '600' }}>87% Confidence</div>
          </div>
          <ProbabilityBar probability={87} label="Bullish" color="var(--accent-green)" />
          <ProbabilityBar probability={9} label="Neutral" color="var(--accent-amber)" />
          <ProbabilityBar probability={4} label="Bearish" color="var(--accent-red)" />
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
