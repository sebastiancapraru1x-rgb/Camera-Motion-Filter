import React from 'react';
import { formatTime, detectionLabel } from '../utils/format';

export default function EventRow({ event }) {
  const dets = event.detections || [];
  const hasDets = dets.length > 0;
  return (
    <tr>
      <td className="ts-col">{formatTime(event.ts)}</td>
      <td className="camera-col">{event.camera_id}</td>
      <td>
        <span className={`badge status-${event.status.toLowerCase()}`}>
          {event.status}
        </span>
      </td>
      <td className="dets">
        {hasDets ? (
          dets.map((d, i) => (
            <span key={i} className="det-chip">
              {d.class} ({Math.round(d.conf * 100)}%)
            </span>
          ))
        ) : (
          <span style={{ color: 'var(--text-dim)' }}>{'—'}</span>
        )}
      </td>
      <td className="video-col">
        {event.video ? event.video.split('/').pop() : '—'}
      </td>
    </tr>
  );
}