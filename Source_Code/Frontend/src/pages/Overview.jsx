import React from 'react';
import { StatCard } from '../components/StatCard';
import { GlassCard } from '../components/GlassCard';
import { MiniChart } from '../components/MiniChart';
import { ProbabilityBar } from '../components/ProbabilityBar';
import { Activity, TrendingUp, Zap, Target } from 'lucide-react';
import { btcData, recentPredictions } from '../data/mockData';

const Overview = () => {
  const currentPrice = btcData[btcData.length - 1].price;
  const prevPrice = btcData[btcData.length - 2].price;
  const change = ((currentPrice - prevPrice) / prevPrice * 100).toFixed(2);

  return (
    <div>
      <h1 className="page-title">Market Overview</h1>
      
      <div className="grid grid-cols-4" style={{ marginBottom: '24px' }}>
        <StatCard 
          title="BTC/USD Price" 
          value={`$${currentPrice.toFixed(2)}`} 
          change={change} 
          isPositive={change >= 0} 
          icon={Activity} 
        />
        <StatCard 
          title="Model Win Rate" 
          value="68.4%" 
          change={2.1} 
          isPositive={true} 
          icon={Target} 
        />
        <StatCard 
          title="Sharpe Ratio" 
          value="2.14" 
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
          <ProbabilityBar probability={82} label="Strong Uptrend" color="var(--accent-green)" />
          <ProbabilityBar probability={14} label="Ranging" color="var(--accent-amber)" />
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
