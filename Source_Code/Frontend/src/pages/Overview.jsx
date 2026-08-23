import React from 'react';
import { StatCard } from '../components/StatCard';
import { GlassCard } from '../components/GlassCard';
import { MiniChart } from '../components/MiniChart';
import { ProbabilityBar } from '../components/ProbabilityBar';
import { Activity, TrendingUp, Zap, Target, Wifi, WifiOff } from 'lucide-react';
import { btcData, recentPredictions } from '../data/mockData';
import { api } from '../api/apiClient';
import { useApi } from '../hooks/useApi';

const Overview = () => {
  const { data: summary } = useApi(() => api.getDashboardSummary(), [], 30000);
  const { data: regime } = useApi(() => api.getRegimeCurrent('BTCUSDT'), [], 30000);
  const { data: latestCandle } = useApi(() => api.getLatestCandle('BTCUSDT'), [], 15000);

  // Use live data if available, otherwise fall back to mock
  const isLive = summary !== null;
  
  const currentPrice = latestCandle ? latestCandle.close : btcData[btcData.length - 1].price;
  const prevPrice = btcData[btcData.length - 2].price;
  const change = ((currentPrice - prevPrice) / prevPrice * 100).toFixed(2);

  const winRate = summary ? `${(summary.overallAccuracy * 100).toFixed(1)}%` : '68.4%';
  const totalPredictions = summary ? summary.totalPredictions.toLocaleString() : '15,000';
  const latestRegime = regime ? regime.regime : 'StrongUptrend';
  const regimeProb = regime ? (regime.probability * 100).toFixed(0) : 82;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <h1 className="page-title" style={{ marginBottom: 0 }}>Market Overview</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', opacity: 0.6 }}>
          {isLive ? <Wifi size={14} color="var(--accent-green)" /> : <WifiOff size={14} color="var(--accent-amber)" />}
          <span>{isLive ? 'Live Data' : 'Mock Data'}</span>
        </div>
      </div>
      
      <div className="grid grid-cols-4" style={{ marginBottom: '24px' }}>
        <StatCard 
          title="BTC/USD Price" 
          value={`$${Number(currentPrice).toFixed(2)}`} 
          change={change} 
          isPositive={change >= 0} 
          icon={Activity} 
        />
        <StatCard 
          title="Model Win Rate" 
          value={winRate} 
          change={2.1} 
          isPositive={true} 
          icon={Target} 
        />
        <StatCard 
          title="Total Predictions" 
          value={totalPredictions} 
          change={0.05} 
          isPositive={true} 
          icon={TrendingUp} 
        />
        <StatCard 
          title="Avg. Confidence" 
          value="82%" 
          change={1.2} 
          isPositive={false} 
          icon={Zap} 
        />
      </div>

      <div className="grid grid-cols-3" style={{ marginBottom: '24px' }}>
        <GlassCard style={{ gridColumn: 'span 2' }}>
          <div style={{ marginBottom: '16px', fontWeight: '600' }}>24H Price Action (BTC)</div>
          <MiniChart data={btcData.slice(-24)} dataKey="price" color="var(--accent-blue)" />
        </GlassCard>

        <GlassCard>
          <div style={{ marginBottom: '16px', fontWeight: '600' }}>Regime Classification</div>
          <ProbabilityBar probability={regimeProb} label={latestRegime} color="var(--accent-green)" />
          <ProbabilityBar probability={100 - regimeProb - 4} label="Ranging" color="var(--accent-amber)" />
          <ProbabilityBar probability={4} label="Downtrend" color="var(--accent-red)" />
        </GlassCard>
      </div>

      <GlassCard>
        <div style={{ marginBottom: '16px', fontWeight: '600' }}>Recent Predictions</div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Asset</th>
              <th>Direction</th>
              <th>Confidence</th>
              <th>Status</th>
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
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{ width: '40px' }}>{pred.confidence}%</div>
                    <div className="prob-bar-container" style={{ width: '60px', marginTop: 0, height: '4px' }}>
                      <div className="prob-bar-fill" style={{ width: `${pred.confidence}%`, background: 'var(--accent-blue)' }}></div>
                    </div>
                  </div>
                </td>
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
  );
};

export default Overview;
