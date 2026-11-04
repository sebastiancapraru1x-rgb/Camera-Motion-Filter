import React from 'react';
import { X, Download, ExternalLink } from 'lucide-react';

export default function AlertModal({ open, filename, onClose }) {
  if (!open || !filename) return null;

  const imageUrl = `/api/alerts/${encodeURIComponent(filename)}`;

  return (
    <div className="modal-overlay" onClick={onClose} role="dialog" aria-modal="true" aria-label="Alert preview">
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title">Alert Preview</div>
          <button className="modal-close" onClick={onClose} aria-label="Close preview">
            <X size={20} strokeWidth={2} />
          </button>
        </div>
        <div className="modal-body">
          <img src={imageUrl} alt={filename} className="modal-image" />
          <div className="modal-meta">
            <div>
              <div className="label">File</div>
              <div>{filename}</div>
            </div>
            <div>
              <div className="label">Source</div>
              <div>API</div>
            </div>
          </div>
        </div>
        <div className="modal-actions">
          <button className="btn-ghost" onClick={onClose}>
            <X size={16} strokeWidth={2} /> Close
          </button>
          <a
            href={imageUrl}
            download={filename}
            className="btn-primary"
            target="_blank"
            rel="noopener noreferrer"
          >
            <Download size={16} strokeWidth={2} /> Download
          </a>
        </div>
      </div>
    </div>
  );
}