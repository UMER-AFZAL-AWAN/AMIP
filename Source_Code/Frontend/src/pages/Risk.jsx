import React from 'react';
import { GlassCard } from '../components/GlassCard';
import { ShieldAlert } from 'lucide-react';

const Risk = () => {
  return (
    <div>
      <h1 className="page-title">Risk Dashboard</h1>

      <div className="grid grid-cols-3" style={{ marginBottom: '24px' }}>
        <GlassCard style={{ textAlign: 'center' }}>
          <ShieldAlert size={48} color="var(--accent-amber)" style={{ margin: '0 auto 16px' }} />
          <h3 style={{ color: 'var(--text-secondary)', marginBottom: '8px' }}>Overall System Risk</h3>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: 'var(--accent-amber)' }}>MEDIUM</div>
          <div style={{ marginTop: '16px', fontSize: '14px', color: 'var(--text-secondary)' }}>
            Elevated volatility detected in major pairs.
          </div>
        </GlassCard>

        <GlassCard style={{ gridColumn: 'span 2' }}>
          <div style={{ marginBottom: '16px', fontWeight: '600' }}>Risk Metrics</div>
          <div className="grid grid-cols-2">
            <div>
              <div style={{ color: 'var(--text-secondary)', marginBottom: '4px' }}>Current Drawdown</div>
              <div style={{ fontSize: '24px', fontWeight: '600', color: 'var(--accent-red)' }}>-4.2%</div>
            </div>
            <div>
              <div style={{ color: 'var(--text-secondary)', marginBottom: '4px' }}>Max Drawdown (30d)</div>
              <div style={{ fontSize: '24px', fontWeight: '600' }}>-8.5%</div>
            </div>
            <div>
              <div style={{ color: 'var(--text-secondary)', marginBottom: '4px' }}>Portfolio Beta</div>
              <div style={{ fontSize: '24px', fontWeight: '600' }}>1.15</div>
            </div>
            <div>
              <div style={{ color: 'var(--text-secondary)', marginBottom: '4px' }}>Recommended Position Size</div>
              <div style={{ fontSize: '24px', fontWeight: '600', color: 'var(--accent-blue)' }}>Reduced (-20%)</div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default Risk;
