import React from 'react';

export const ProbabilityBar = ({ probability, label, color }) => {
  return (
    <div style={{ marginBottom: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px', fontSize: '14px' }}>
        <span>{label}</span>
        <span style={{ fontWeight: '600' }}>{probability}%</span>
      </div>
      <div className="prob-bar-container">
        <div className="prob-bar-fill" style={{ width: `${probability}%`, background: color }}></div>
      </div>
    </div>
  );
};
