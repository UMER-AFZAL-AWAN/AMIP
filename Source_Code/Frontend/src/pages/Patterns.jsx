import React from 'react';
import { GlassCard } from '../components/GlassCard';
import { patterns } from '../data/mockData';

const Patterns = () => {
  return (
    <div>
      <h1 className="page-title">Pattern Recognition</h1>

      <div className="grid grid-cols-3">
        {patterns.map(p => (
          <GlassCard key={p.id}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
              <div style={{ fontWeight: '600', fontSize: '18px' }}>{p.name}</div>
              <span className="badge badge-blue">{p.timeframe}</span>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', color: 'var(--text-secondary)' }}>
              <span>Asset</span>
              <span style={{ color: 'var(--text-primary)' }}>{p.asset}</span>
            </div>
            
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '16px', color: 'var(--text-secondary)' }}>
              <span>Expected Outcome</span>
              <span className={p.expectedOutcome === 'BULLISH' ? 'text-green' : 'text-red'} style={{ fontWeight: 'bold' }}>
                {p.expectedOutcome}
              </span>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '4px' }}>
                <span>Similarity Score</span>
                <span>{p.similarity}%</span>
              </div>
              <div className="prob-bar-container" style={{ height: '6px' }}>
                <div className="prob-bar-fill" style={{ width: `${p.similarity}%`, background: p.similarity > 90 ? 'var(--accent-green)' : 'var(--accent-amber)' }}></div>
              </div>
            </div>
          </GlassCard>
        ))}
      </div>
    </div>
  );
};

export default Patterns;
