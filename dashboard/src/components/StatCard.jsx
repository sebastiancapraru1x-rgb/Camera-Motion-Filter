import React from 'react';
import { TrendingUp, TrendingDown, AlertCircle, HardDrive, Users } from 'lucide-react';

const ICONS = {
  slate: Users,
  green: TrendingUp,
  red: AlertCircle,
  amber: HardDrive,
  blue: Users,
};

export default function StatCard({ label, value, accent, subtext, trend, trendValue }) {
  const Icon = ICONS[accent] || Users;
  const trendColor = trend === 'up' ? 'trend-up' : trend === 'down' ? 'trend-down' : 'trend-neutral';
  return (
    <div className={`stat-card ${accent}`}>
      <div className="stat-header">
        <div className="stat-label">{label}</div>
        <Icon className="stat-icon" aria-hidden="true" />
      </div>
      <div className="stat-value">{value}</div>
      {subtext && <div className="stat-subtext">{subtext}</div>}
      {trend && trendValue && (
        <div className={`stat-trend ${trendColor}`}>
          <span>{trend}</span>
          <span>{trendValue}</span>
        </div>
      )}
    </div>
  );
}