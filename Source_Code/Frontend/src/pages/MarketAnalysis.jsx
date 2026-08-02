import React from 'react';
import { GlassCard } from '../components/GlassCard';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { btcData } from '../data/mockData';

const MarketAnalysis = () => {
  return (
    <div>
      <h1 className="page-title">Market Analysis</h1>
      
      <div className="grid" style={{ gap: '24px' }}>
        <GlassCard>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
            <div style={{ fontWeight: '600', fontSize: '18px' }}>BTC/USD Advanced Chart</div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <span className="badge badge-blue">1H</span>
              <span className="badge" style={{ background: 'var(--glass-bg)' }}>4H</span>
              <span className="badge" style={{ background: 'var(--glass-bg)' }}>1D</span>
            </div>
          </div>
          <div style={{ height: '400px', width: '100%' }}>
            <ResponsiveContainer>
              <AreaChart data={btcData}>
                <defs>
                  <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--accent-blue)" stopOpacity={0.4}/>
                    <stop offset="95%" stopColor="var(--accent-blue)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis dataKey="time" stroke="var(--text-secondary)" />
                <YAxis domain={['auto', 'auto']} stroke="var(--text-secondary)" />
                <Tooltip 
                  contentStyle={{ background: 'rgba(10,14,39,0.9)', border: '1px solid rgba(255,255,255,0.1)' }}
                  itemStyle={{ color: '#fff' }}
                />
                <Area type="monotone" dataKey="price" stroke="var(--accent-blue)" fillOpacity={1} fill="url(#colorPrice)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </GlassCard>

        <div className="grid grid-cols-2">
          <GlassCard>
            <div style={{ marginBottom: '16px', fontWeight: '600' }}>Volume Profile</div>
            <div style={{ height: '200px' }}>
              <ResponsiveContainer>
                <BarChart data={btcData.slice(-30)}>
                  <Tooltip contentStyle={{ background: 'rgba(10,14,39,0.9)', border: 'none' }} />
                  <Bar dataKey="volume" fill="var(--accent-blue)" opacity={0.6} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </GlassCard>

          <GlassCard>
            <div style={{ marginBottom: '16px', fontWeight: '600' }}>Feature Importance Heatmap</div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '8px', height: '200px' }}>
              {Array.from({ length: 16 }).map((_, i) => {
                const intensity = Math.random();
                const r = Math.floor(0 * intensity);
                const g = Math.floor(212 * intensity);
                const b = Math.floor(255 * intensity);
                return (
                  <div key={i} style={{ 
                    background: `rgba(${r}, ${g}, ${b}, ${intensity + 0.1})`, 
                    borderRadius: '4px',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    fontSize: '12px', color: intensity > 0.5 ? '#fff' : 'rgba(255,255,255,0.3)'
                  }}>
                    F{i+1}
                  </div>
                );
              })}
            </div>
          </GlassCard>
        </div>
      </div>
    </div>
  );
};

export default MarketAnalysis;
