import React from 'react';
import { Video, AlertCircle } from 'lucide-react';

export default function EmptyState({ type = 'events', message }) {
  const Icon = type === 'events' ? Video : AlertCircle;
  const defaults = {
    events: {
      title: 'No events yet',
      desc: 'Start analyzing video clips to see motion detection events here.',
    },
    alerts: {
      title: 'No alert thumbnails yet',
      desc: 'Real-motion detections will appear here with best-frame thumbnails.',
    },
  };
  const d = defaults[type] || defaults.events;
  return (
    <div className="empty-state" role="status" aria-label={d.title}>
      <Icon className="empty-icon" aria-hidden="true" />
      <h3 className="empty-title">{message || d.title}</h3>
      <p className="empty-desc">{message ? '' : d.desc}</p>
    </div>
  );
}