import React from 'react';
import { RefreshCw, Bell, Monitor, Server } from 'lucide-react';
import StatusIndicator from './StatusIndicator';
import RefreshButton from './RefreshButton';

export default function Header({ backendOnline, onRefresh, refreshLoading, autoRefresh, onToggleAutoRefresh }) {
  return (
    <header className="app-header">
      <div className="header-left">
        <div className="brand">
          <span className="brand-dot" aria-hidden="true" />
          AI Camera
          <span className="brand-tag">v1.0.0</span>
        </div>
      </div>
      <div className="header-center">
        <StatusIndicator online={backendOnline} />
        <RefreshButton onClick={onRefresh} loading={refreshLoading} />
      </div>
      <div className="auto-refresh">
        <label style={{ display: 'flex', alignItems: 'center', gap: 8, cursor: 'pointer' }}>
          <div className={`toggle ${autoRefresh ? 'active' : ''}`} onClick={onToggleAutoRefresh} role="switch" aria-checked={autoRefresh} />
          <span className="toggle-label">Auto-refresh</span>
        </label>
      </div>
    </header>
  );
}