import React from 'react';
import { GlassCard } from './GlassCard';

export const StatCard = ({ title, value, change, isPositive, icon: Icon }) => {
  return (
    <GlassCard className="stat-card">
      <div className="stat-header">
        <span>{title}</span>
        {Icon && <Icon size={18} />}
      </div>
      <div className="stat-value">{value}</div>
      <div className={`stat-change ${isPositive ? 'text-green' : 'text-red'}`}>
        {isPositive ? '▲' : '▼'} {Math.abs(change)}%
      </div>
    </GlassCard>
  );
};
