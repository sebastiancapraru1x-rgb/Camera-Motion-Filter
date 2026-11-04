import React from 'react';

export default function DiskUsage({ usedGB, capGB = 3 }) {
  const pct = capGB > 0 ? Math.min((usedGB / capGB) * 100, 100) : 0;
  const safe = pct < 80;
  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-title">
          <span className="panel-icon" style={{ color: 'var(--accent-amber)' }} aria-hidden="true">&#9650;</span>
          Disk Usage
        </div>
        <div className="panel-subtitle">{`${usedGB.toFixed(2)} / ${capGB} GB`}</div>
      </div>
      <div className="panel-body" style={{ paddingBottom: 8 }}>
        <div className="disk-gauge">
          <div
            className={`disk-fill ${safe ? 'safe' : ''}`}
            style={{ width: `${pct}%` }}
            role="progressbar"
            aria-valuenow={pct}
            aria-valuemin={0}
            aria-valuemax={100}
          />
        </div>
        <div className="disk-stats">
          <span>{safe ? 'Within limit' : 'Approaching cap'}</span>
          <span>{`${Math.round(pct)}% used`}</span>
        </div>
      </div>
    </div>
  );
}