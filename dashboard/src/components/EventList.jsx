import React from 'react';

const STATUS_BADGE = {
  TRUE: 'status-true',
  FALSE: 'status-false',
};

export default function EventList({ events }) {
  if (!events || events.length === 0) {
    return <div className="empty">No events yet.</div>;
  }
  return (
    <table className="event-table">
      <thead>
        <tr>
          <th>Time</th>
          <th>Camera</th>
          <th>Status</th>
          <th>Detections</th>
          <th>Video</th>
        </tr>
      </thead>
      <tbody>
        {events.map((e) => (
          <tr key={e.ts}>
            <td className="ts">{new Date(e.ts).toLocaleTimeString()}</td>
            <td className="camera">{e.camera_id}</td>
            <td>
              <span className={`badge ${STATUS_BADGE[e.status]}`}>{e.status}</span>
            </td>
            <td className="dets">
              {(e.detections || []).map((d, i) => (
                <span key={i}>{d.class} ({Math.round(d.conf * 100)}%)</span>
              ))}
            </td>
            <td className="video">{e.video ? e.video.split('/').pop() : '—'}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}