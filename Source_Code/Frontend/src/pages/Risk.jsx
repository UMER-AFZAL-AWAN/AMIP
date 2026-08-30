import React from 'react';
import { GlassCard } from '../components/GlassCard';
import { ShieldAlert, ShieldCheck, Wifi, WifiOff } from 'lucide-react';
import { api } from '../api/apiClient';
import { useApi } from '../hooks/useApi';

const Risk = () => {
  const { data: latestPrediction } = useApi(() => api.getLatestPrediction('BTCUSDT'), [], 15000);

  const isLive = latestPrediction !== null;

  const riskScore = latestPrediction ? latestPrediction.risk : 0.42;
  const riskLevel = riskScore > 0.65 ? 'HIGH' : riskScore > 0.35 ? 'MEDIUM' : 'LOW';
  const riskColor = riskLevel === 'HIGH' ? 'var(--accent-red)' : riskLevel === 'MEDIUM' ? 'var(--accent-amber)' : 'var(--accent-green)';
  const RiskIcon = riskLevel === 'LOW' ? ShieldCheck : ShieldAlert;

  const positionSizeAdj = riskLevel === 'HIGH' ? 'Reduced (-50%)' : riskLevel === 'MEDIUM' ? 'Reduced (-20%)' : 'Standard (100%)';

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <h1 className="page-title" style={{ marginBottom: 0 }}>Risk Dashboard</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', opacity: 0.6 }}>
          {isLive ? <Wifi size={14} color="var(--accent-green)" /> : <WifiOff size={14} color="var(--accent-amber)" />}
          <span>{isLive ? 'Live Risk Engine' : 'Mock Data'}</span>
        </div>
      </div>

      <div className="grid grid-cols-3" style={{ marginBottom: '24px' }}>
        <GlassCard style={{ textAlign: 'center' }}>
          <RiskIcon size={48} color={riskColor} style={{ margin: '0 auto 16px' }} />
          <h3 style={{ color: 'var(--text-secondary)', marginBottom: '8px' }}>Overall System Risk</h3>
          <div style={{ fontSize: '32px', fontWeight: 'bold', color: riskColor }}>{riskLevel}</div>
          <div style={{ marginTop: '16px', fontSize: '14px', color: 'var(--text-secondary)' }}>
            {isLive
              ? `Entropy risk metric: ${(riskScore * 100).toFixed(1)}% on latest candle.`
              : 'Elevated volatility detected in major pairs.'}
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
              <div style={{ fontSize: '24px', fontWeight: '600', color: 'var(--accent-blue)' }}>{positionSizeAdj}</div>
            </div>
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default Risk;
