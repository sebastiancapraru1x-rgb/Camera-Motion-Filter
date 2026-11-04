import React from 'react';
import { AlertCircle, CheckCircle } from 'lucide-react';

export default function Toast({ type = 'error', message, onClose }) {
  const Icon = type === 'error' ? AlertCircle : CheckCircle;
  return (
    <div className={`toast ${type}`} role="alert" aria-live="polite">
      <Icon className="toast-icon" />
      <span>{message}</span>
      <button
        className="btn-ghost"
        onClick={onClose}
        style={{ padding: 2, marginLeft: 'auto', opacity: 0.5 }}
      >
        ×
      </button>
    </div>
  );
}