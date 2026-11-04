export function formatTime(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

export function formatDate(iso) {
  if (!iso) return '—';
  return new Date(iso).toLocaleDateString([], { month: 'short', day: 'numeric' });
}

export function formatBytes(bytes) {
  if (!bytes && bytes !== 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${(bytes / Math.pow(k, i)).toFixed(2)} ${sizes[i]}`;
}

export function formatPercent(n, decimals = 0) {
  if (n == null) return '0%';
  return `${n.toFixed(decimals)}%`;
}

export function truncate(str, len = 30) {
  if (!str) return '—';
  if (str.length <= len) return str;
  return str.slice(0, len) + '…';
}

export function detectionLabel(dets) {
  if (!dets || dets.length === 0) return 'none';
  return dets.map(d => `${d.class} (${Math.round(d.conf * 100)}%)`).join(', ');
}

export function statusColor(status) {
  return status === 'TRUE' ? 'var(--accent-green)' : 'var(--accent-red)';
}
