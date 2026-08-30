import React from 'react';
import { GlassCard } from '../components/GlassCard';
import { patterns as mockPatterns } from '../data/mockData';
import { api } from '../api/apiClient';
import { useApi } from '../hooks/useApi';
import { Wifi, WifiOff } from 'lucide-react';

const Patterns = () => {
  const { data: livePatterns } = useApi(() => api.getSimilarPatterns('BTCUSDT', 6), [], 30000);

  const isLive = livePatterns !== null && Array.isArray(livePatterns) && livePatterns.length > 0;

  const patternList = isLive
    ? livePatterns.map((p, idx) => ({
        id: p.id || `p-${idx}`,
        name: p.patternId || `Pattern Cluster #${p.clusterId ?? idx + 1}`,
        timeframe: '15m',
        asset: 'BTC',
        expectedOutcome: (p.successRate ?? 0.5) >= 0.5 ? 'BULLISH' : 'BEARISH',
        similarity: p.successRate != null ? Math.round(p.successRate * 100) : 85,
      }))
    : mockPatterns;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <h1 className="page-title" style={{ marginBottom: 0 }}>Pattern Recognition</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', opacity: 0.6 }}>
          {isLive ? <Wifi size={14} color="var(--accent-green)" /> : <WifiOff size={14} color="var(--accent-amber)" />}
          <span>{isLive ? 'Live Pattern Engine' : 'Mock Data'}</span>
        </div>
      </div>

      <div className="grid grid-cols-3">
        {patternList.map(p => (
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
