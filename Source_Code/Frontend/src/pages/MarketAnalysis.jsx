import React, { useMemo } from 'react';
import { GlassCard } from '../components/GlassCard';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { btcData } from '../data/mockData';
import { api } from '../api/apiClient';
import { useApi } from '../hooks/useApi';
import { Wifi, WifiOff } from 'lucide-react';

const MarketAnalysis = () => {
  const now = new Date().toISOString();
  const dayAgo = new Date(Date.now() - 24 * 3600 * 1000).toISOString();
  
  const { data: liveCandles } = useApi(
    () => api.getCandles('BTCUSDT', 'Binance', 'OneMinute', dayAgo, now), [], 30000
  );

  const chartData = useMemo(() => {
    if (liveCandles && liveCandles.length > 0) {
      return liveCandles.map(c => ({
        time: new Date(c.closeTime).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        price: c.close,
        volume: c.volume,
        open: c.open,
        high: c.high,
        low: c.low,
      }));
    }
    return btcData;
  }, [liveCandles]);

  const isLive = liveCandles !== null && liveCandles.length > 0;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <h1 className="page-title" style={{ marginBottom: 0 }}>Market Analysis</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', opacity: 0.6 }}>
          {isLive ? <Wifi size={14} color="var(--accent-green)" /> : <WifiOff size={14} color="var(--accent-amber)" />}
          <span>{isLive ? `Live (${chartData.length} candles)` : 'Mock Data'}</span>
        </div>
      </div>
      
      <div className="grid" style={{ gap: '24px' }}>
        <GlassCard>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '24px' }}>
            <div style={{ fontWeight: '600', fontSize: '18px' }}>BTC/USD Advanced Chart</div>
            <div style={{ display: 'flex', gap: '8px' }}>
              <span className="badge badge-blue">1M</span>
              <span className="badge" style={{ background: 'var(--glass-bg)' }}>1H</span>
              <span className="badge" style={{ background: 'var(--glass-bg)' }}>4H</span>
            </div>
          </div>
          <div style={{ height: '400px', width: '100%' }}>
            <ResponsiveContainer>
              <AreaChart data={chartData}>
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
                <BarChart data={chartData.slice(-30)}>
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
