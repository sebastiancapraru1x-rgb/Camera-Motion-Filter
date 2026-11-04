import React, { useState, useEffect, useCallback } from 'react';
import { useApi } from './hooks/useApi';
import { formatBytes } from './utils/format';
import Header from './components/Header';
import StatsGrid from './components/StatsGrid';
import CameraStatus from './components/CameraStatus';
import DiskUsage from './components/DiskUsage';
import RecentEvents from './components/RecentEvents';
import AlertGallery from './components/AlertGallery';
import EmptyState from './components/EmptyState';
import Toast from './components/Toast';
import { RefreshCw, Monitor, LayoutDashboard } from 'lucide-react';

const REFRESH_INTERVAL_MS = 60000;

export default function App() {
  const { request } = useApi();
  const [stats, setStats] = useState(null);
  const [events, setEvents] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [backendOnline, setBackendOnline] = useState(false);
  const [refreshLoading, setRefreshLoading] = useState(false);
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [toasts, setToasts] = useState([]);
  const [activeCamera, setActiveCamera] = useState('all');
  const [lastRefresh, setLastRefresh] = useState(null);

  const addToast = useCallback((type, message) => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, type, message }]);
    setTimeout(() => setToasts((prev) => prev.filter((t) => t.id !== id)), 5000);
  }, []);

  const fetchHealth = useCallback(async () => {
    try {
      await request('/health');
      setBackendOnline(true);
    } catch {
      setBackendOnline(false);
    }
  }, [request]);

  const fetchStats = useCallback(async () => {
    try {
      const data = await request('/stats');
      setStats(data);
      setAlerts(data.alerts || []);
    } catch (err) {
      addToast('error', `Failed to load stats: ${err.message}`);
    }
  }, [request, addToast]);

  const fetchEvents = useCallback(async () => {
    try {
      const data = await request('/events?limit=50');
      setEvents(Array.isArray(data) ? data : []);
    } catch (err) {
      addToast('error', `Failed to load events: ${err.message}`);
    }
  }, [request, addToast]);

  const fetchAll = useCallback(async () => {
    setRefreshLoading(true);
    try {
      await Promise.all([fetchHealth(), fetchStats(), fetchEvents()]);
      setLastRefresh(new Date());
    } finally {
      setRefreshLoading(false);
    }
  }, [fetchHealth, fetchStats, fetchEvents]);

  useEffect(() => {
    fetchAll();
  }, [fetchAll]);

  useEffect(() => {
    const id = setInterval(fetchHealth, 30000);
    return () => clearInterval(id);
  }, [fetchHealth]);

  useEffect(() => {
    if (!autoRefresh) return;
    const id = setInterval(fetchAll, REFRESH_INTERVAL_MS);
    return () => clearInterval(id);
  }, [autoRefresh, fetchAll]);

  const handleRefresh = () => { fetchAll(); };
  const handleToggleAutoRefresh = () => {
    setAutoRefresh((prev) => {
      const next = !prev;
      addToast(next ? 'success' : 'info', `Auto-refresh ${next ? 'enabled' : 'disabled'}`);
      return next;
    });
  };

  const diskUsageMB = stats?.disk_usage_mb ?? 0;

  return (
    <div className="app">
      <Header
        backendOnline={backendOnline}
        onRefresh={handleRefresh}
        refreshLoading={refreshLoading}
        autoRefresh={autoRefresh}
        onToggleAutoRefresh={handleToggleAutoRefresh}
      />
      <main className="app-main">
        {!backendOnline ? (
          <div className="panel-card" style={{ height: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <div className="empty-state">
              <Monitor size={64} strokeWidth={2} style={{ color: 'var(--accent-red)' }} />
              <h3 className="empty-title">Backend offline</h3>
              <p className="empty-desc">
                The FastAPI receiver is not reachable at http://localhost:8000. Start it with:{' '}
                <code>uvicorn src.api.server:app --host 0.0.0.0 --port 8000</code>
              </p>
              <button className="btn-primary" onClick={handleRefresh} style={{ marginTop: 16 }}>
                <RefreshCw size={16} strokeWidth={2} /> Retry
              </button>
            </div>
          </div>
        ) : (
          <>
            <StatsGrid stats={stats} />
            <CameraStatus
              cameras={[
                { id: 'default', name: 'Driveway', online: backendOnline, count: stats?.true || 0 },
                { id: 'backyard', name: 'Backyard', online: backendOnline, count: stats?.false || 0 },
              ]}
              activeCamera={activeCamera}
              setActiveCamera={setActiveCamera}
            />
            <div className="dashboard-grid">
              <div className="panel-card" style={{ minHeight: 400 }}>
                <div className="panel-header">
                  <div className="panel-title">
                    <span className="panel-icon" style={{ color: 'var(--accent-blue)' }} aria-hidden="true">
                      <LayoutDashboard size={18} strokeWidth={2} />
                    </span>
                    Recent Events
                  </div>
                  <div className="panel-subtitle">{events.length} event{events.length !== 1 ? 's' : ''}</div>
                </div>
                <div className="panel-body" style={{ padding: 0 }}>
                  {events.length === 0 ? (
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
                        {events.map((e) => (
                          <tr key={e.ts}>
                            <td className="ts-col">{new Date(e.ts).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</td>
                            <td className="camera-col">{e.camera_id}</td>
                            <td>
                              <span className={`badge status-${e.status.toLowerCase()}`}>{e.status}</span>
                            </td>
                            <td className="dets">
                              {(e.detections || []).map((d, i) => (
                                <span key={i} className="det-chip">
                                  {d.class} ({Math.round(d.conf * 100)}%)
                                </span>
                              ))}
                            </td>
                            <td className="video-col">{e.video ? e.video.split('/').pop() : '—'}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  )}
                </div>
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
                <AlertGallery alerts={alerts} />
                <div className="panel-card">
                  <div className="panel-header">
                    <div className="panel-title">
                      <span className="panel-icon" style={{ color: 'var(--accent-amber)' }} aria-hidden="true">
                        <svg width="18" height="18" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2" /></svg>
                      </span>
                      Storage
                    </div>
                    <div className="panel-subtitle">{formatBytes(diskUsageMB * 1024 * 1024)}</div>
                  </div>
                  <div className="panel-body">
                    <DiskUsage usedGB={diskUsageMB / 1024} capGB={stats?.disk_cap_gb || 3} />
                  </div>
                </div>
              </div>
            </div>
          </>
        )}
      </main>
      <div className="toast-container" aria-live="polite" aria-atomic="true">
        {toasts.map((t) => (
          <Toast key={t.id} type={t.type} message={t.message} onClose={() => setToasts((prev) => prev.filter((x) => x.id !== t.id))} />
        ))}
      </div>
    </div>
  );
}
