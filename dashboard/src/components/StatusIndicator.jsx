import React from 'react';

export default function StatusIndicator({ online }) {
  return (
    <div className="system-status">
      <span className={`status-dot ${online ? '' : 'offline'}`} aria-hidden="true" />
      <span className="status-text" aria-label={online ? 'Backend online' : 'Backend offline'}>
        {online ? 'BACKEND ONLINE' : 'BACKEND OFFLINE'}
      </span>
    </div>
  );
}