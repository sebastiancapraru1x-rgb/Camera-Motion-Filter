import React from 'react';
import { Image, Maximize } from 'lucide-react';
import AlertModal from './AlertModal';

export default function AlertGallery({ alerts, onSelect }) {
  const [selected, setSelected] = React.useState(null);

  if (!alerts || alerts.length === 0) {
    return (
      <div className="panel-card">
        <div className="panel-header">
          <div className="panel-title">
            <span className="panel-icon" style={{ color: 'var(--accent-purple)' }} aria-hidden="true">
              <Image size={18} strokeWidth={2} />
            </span>
            Alert Thumbnails
          </div>
          <div className="panel-subtitle">0 alerts</div>
        </div>
        <div className="panel-body">
          <div className="empty-state">
            <div className="empty-icon" aria-hidden="true">
              <Image size={48} strokeWidth={2} />
            </div>
            <h3 className="empty-title">No alert thumbnails yet</h3>
            <p className="empty-desc">Real-motion detections will appear here with best-frame thumbnails.</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="panel-card">
        <div className="panel-header">
          <div className="panel-title">
            <span className="panel-icon" style={{ color: 'var(--accent-purple)' }} aria-hidden="true">
              <Image size={18} strokeWidth={2} />
            </span>
            Alert Thumbnails
          </div>
          <div className="panel-subtitle">{alerts.length} alert{alerts.length !== 1 ? 's' : ''}</div>
        </div>
        <div className="panel-body">
          <div className="gallery-grid">
            {alerts.map((name) => (
              <div
                key={name}
                className="gallery-item"
                onClick={() => {
                  setSelected(name);
                  onSelect?.(name);
                }}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => e.key === 'Enter' && setSelected(name)}
              >
                <img
                  src={"/api/alerts/" + encodeURIComponent(name)}
                  alt={name}
                  className="gallery-img"
                  loading="lazy"
                />
                <div className="gallery-overlay">
                  <span className="gallery-name">{name}</span>
                  <Maximize size={14} strokeWidth={2} style={{ opacity: 0.8 }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
      <AlertModal
        open={selected != null}
        filename={selected}
        onClose={() => setSelected(null)}
      />
    </>
  );
}
