import React from 'react';
import { Camera } from 'lucide-react';

export default function CameraStatus({ cameras, activeCamera, setActiveCamera }) {
  if (!cameras || cameras.length === 0) {
    return (
      <div className="camera-card" style={{ opacity: 0.5, cursor: 'default' }}>
        <Camera className="camera-dot" style={{ width: 16, height: 16, color: 'var(--text-dim)' }} />
        <span className="camera-name">No cameras</span>
      </div>
    );
  }
  return (
    <div className="cameras-strip" role="tablist" aria-label="Camera selection">
      {cameras.map((cam) => {
        const isActive = activeCamera === cam.id;
        return (
          <button
            key={cam.id}
            className={`camera-card ${isActive ? 'active' : ''}`}
            onClick={() => setActiveCamera(cam.id)}
            role="tab"
            aria-selected={isActive}
          >
            <span className={`camera-dot ${cam.online ? '' : 'offline'}`} aria-hidden="true" />
            <span className="camera-name">{cam.name}</span>
            {cam.count != null && (
              <span className="camera-count">{cam.count}</span>
            )}
          </button>
        );
      })}
    </div>
  );
}