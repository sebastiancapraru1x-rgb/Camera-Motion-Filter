import React from 'react';
import { RefreshCw } from 'lucide-react';

export default function RefreshButton({ onClick, loading }) {
  return (
    <button
      className={`refresh-btn ${loading ? 'loading' : ''}`}
      onClick={onClick}
      aria-label={loading ? 'Refreshing…' : 'Refresh data'}
    >
      <RefreshCw className="refresh-icon" />
      <span>{loading ? 'Refreshing…' : 'Refresh'}</span>
    </button>
  );
}