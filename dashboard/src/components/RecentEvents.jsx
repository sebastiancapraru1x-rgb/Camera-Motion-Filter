import React from 'react';
import { List, Clock } from 'lucide-react';
import EmptyState from './EmptyState';
import EventRow from './EventRow';

export default function RecentEvents({ events, cameraFilter }) {
  const filtered = events.filter((e) => {
    if (!cameraFilter || cameraFilter === 'all') return true;
    return e.camera_id === cameraFilter;
  });

  return (
    <div className="panel-card">
      <div className="panel-header">
        <div className="panel-title">
          <span className="panel-icon" style={{ color: 'var(--accent-blue)' }} aria-hidden="true">
            <List size={18} strokeWidth={2} />
          </span>
          Recent Events
        </div>
        <div className="panel-subtitle">{filtered.length} event{filtered.length !== 1 ? 's' : ''}</div>
      </div>
      <div className="panel-body" style={{ padding: 0 }}>
        {filtered.length === 0 ? (
          <EmptyState type="events" />
        ) : (
          <table className="event-table">
            <thead>
              <tr>
                <th style={{ width: '70px' }}>Time</th>
                <th>Camera</th>
                <th style={{ width: '90px' }}>Status</th>
                <th style={{ width: '180px' }}>Detections</th>
                <th>Video</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((e) => (
                <EventRow key={e.ts} event={e} />
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}