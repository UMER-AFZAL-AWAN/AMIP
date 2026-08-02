import React from 'react';
import { AreaChart, Area, ResponsiveContainer, Tooltip } from 'recharts';

export const MiniChart = ({ data, dataKey, color }) => {
  return (
    <div style={{ width: '100%', height: 60 }}>
      <ResponsiveContainer>
        <AreaChart data={data}>
          <defs>
            <linearGradient id={`color-${dataKey}`} x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor={color} stopOpacity={0.3}/>
              <stop offset="95%" stopColor={color} stopOpacity={0}/>
            </linearGradient>
          </defs>
          <Tooltip 
            contentStyle={{ background: 'rgba(10,14,39,0.8)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
            itemStyle={{ color: '#fff' }}
            labelStyle={{ display: 'none' }}
          />
          <Area type="monotone" dataKey={dataKey} stroke={color} fillOpacity={1} fill={`url(#color-${dataKey})`} />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
