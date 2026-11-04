import React from 'react';
import StatCard from './StatCard';

export default function StatsGrid({ stats }) {
  if (!stats) return null;

  const falseRate = stats.false_rate != null ? (stats.false_rate * 100).toFixed(1) : 0;
  const diskUsage = stats.disk_usage_mb != null ? (stats.disk_usage_mb / 1024).toFixed(2) : 0;

  return (
    <div className="stats-grid">
      <StatCard
        label="Total Events"
        value={stats.total}
        accent="slate"
        subtext="All detections"
        trend={stats.total > 0 ? 'up' : 'neutral'}
        trendValue={stats.total}
      />
      <StatCard
        label="Real Alerts"
        value={stats.true}
        accent="green"
        subtext="Confirmed motion"
        trend={stats.true > 0 ? 'up' : 'neutral'}
        trendValue={`${stats.true} detected`}
      />
      <StatCard
        label="False Alarms"
        value={stats.false}
        accent="red"
        subtext="Filtered events"
        trend={stats.false > 0 ? 'down' : 'neutral'}
        trendValue={`${stats.false} blocked`}
      />
      <StatCard
        label="False Rate"
        value={falseRate + '%'}
        accent="amber"
        subtext="False / total"
      />
      <StatCard
        label="Disk Usage"
        value={diskUsage + ' GB'}
        accent="blue"
        subtext={`of ${stats.disk_cap_gb || 3} GB cap`}
      />
    </div>
  );
}