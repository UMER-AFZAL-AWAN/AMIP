import React from 'react';
import { GlassCard } from '../components/GlassCard';
import { models as mockModels } from '../data/mockData';
import { api } from '../api/apiClient';
import { useApi } from '../hooks/useApi';
import { Wifi, WifiOff } from 'lucide-react';

const STATUS_MAP = { 0: 'INACTIVE', 1: 'TRAINING', 2: 'ACTIVE' };

const Models = () => {
  const { data: liveRegistry } = useApi(() => api.getModelRegistry(), [], 30000);

  const isLive = liveRegistry !== null && Array.isArray(liveRegistry) && liveRegistry.length > 0;

  const modelList = isLive
    ? liveRegistry.map((m, idx) => ({
        id: m.id || `m-${idx}`,
        name: m.name,
        version: m.version,
        status: STATUS_MAP[m.status] || (typeof m.status === 'string' ? m.status : 'ACTIVE'),
        accuracy: m.accuracy != null ? (m.accuracy * 100).toFixed(1) : 68.4,
        deployed: m.registeredAt ? new Date(m.registeredAt).toISOString().split('T')[0] : '2026-08-01',
      }))
    : mockModels;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
        <h1 className="page-title" style={{ marginBottom: 0 }}>Model Registry</h1>
        <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '12px', opacity: 0.6 }}>
          {isLive ? <Wifi size={14} color="var(--accent-green)" /> : <WifiOff size={14} color="var(--accent-amber)" />}
          <span>{isLive ? 'Live Registry' : 'Mock Data'}</span>
        </div>
      </div>

      <GlassCard style={{ marginBottom: '24px' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Model Name</th>
              <th>Version</th>
              <th>Status</th>
              <th>Accuracy (30d)</th>
              <th>Deployed</th>
            </tr>
          </thead>
          <tbody>
            {modelList.map(m => (
              <tr key={m.id}>
                <td style={{ fontWeight: '500' }}>{m.name}</td>
                <td>{m.version}</td>
                <td>
                  <span className={`badge ${m.status === 'ACTIVE' ? 'badge-green' : m.status === 'TRAINING' ? 'badge-amber' : 'badge-red'}`}>
                    {m.status}
                  </span>
                </td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span>{m.accuracy}%</span>
                    <div className="prob-bar-container" style={{ width: '100px', marginTop: 0, height: '4px' }}>
                      <div className="prob-bar-fill" style={{ width: `${m.accuracy}%`, background: 'var(--accent-blue)' }}></div>
                    </div>
                  </div>
                </td>
                <td>{m.deployed}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </GlassCard>

      <div className="grid grid-cols-2">
        <GlassCard>
          <div style={{ marginBottom: '16px', fontWeight: '600' }}>Training Experiments</div>
          <div style={{ padding: '16px', background: 'var(--glass-bg)', borderRadius: '8px', fontFamily: 'monospace', fontSize: '13px', color: 'var(--accent-green)' }}>
            <div>&gt; Epoch 45/100: loss=0.2341, val_loss=0.2511</div>
            <div>&gt; Epoch 46/100: loss=0.2305, val_loss=0.2489</div>
            <div>&gt; Epoch 47/100: loss=0.2281, val_loss=0.2475</div>
            <div style={{ color: 'var(--accent-amber)' }}>&gt; Warning: Validation loss plateauing...</div>
            <div className="status-dot" style={{ display: 'inline-block', width: '6px', height: '6px', marginRight: '8px' }}></div>
            Training in progress...
          </div>
        </GlassCard>
      </div>
    </div>
  );
};

export default Models;
