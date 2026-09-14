import React from 'react';
import StatCard from '../components/StatCard.jsx';
import SeverityBadge from '../components/SeverityBadge.jsx';
import './Dashboard.css';

function Dashboard({ bugs, onNavigate }) {
  const totalBugs = bugs.length;
  const criticalBugs = bugs.filter((b) => b.severity?.toLowerCase() === 'critical').length;
  const highBugs = bugs.filter((b) => b.severity?.toLowerCase() === 'high').length;
  const duplicateBugs = bugs.filter((b) => b.isDuplicate).length;

  const recentBugs = [...bugs].slice(0, 5);

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Triage Overview</h1>
          <p className="page-subtitle">Real-time breakdown of reported issues and AI severity classifications.</p>
        </div>
        <button className="primary-action-btn" onClick={() => onNavigate('submit')}>
          <span className="btn-icon">+</span> Report New Bug
        </button>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Bugs"
          value={totalBugs}
          subtitle="All recorded triage cases"
          icon="📊"
          variant="primary"
        />
        <StatCard
          title="Critical Bugs"
          value={criticalBugs}
          subtitle="Immediate remediation required"
          icon="🚨"
          variant="critical"
        />
        <StatCard
          title="High Severity"
          value={highBugs}
          subtitle="High priority sprint items"
          icon="⚠️"
          variant="high"
        />
        <StatCard
          title="Duplicate Bugs"
          value={duplicateBugs}
          subtitle="Identified redundant issues"
          icon="🔄"
          variant="duplicate"
        />
      </div>

      <div className="recent-section">
        <div className="section-header">
          <div className="section-header-left">
            <h2 className="section-title">Recent Bugs</h2>
            <span className="section-count">{recentBugs.length} latest</span>
          </div>
          <button className="text-action-btn" onClick={() => onNavigate('history')}>
            View All in Bug History →
          </button>
        </div>

        <div className="table-wrapper">
          <table className="bugs-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Bug Title</th>
                <th>Environment</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Reported Date</th>
              </tr>
            </thead>
            <tbody>
              {recentBugs.map((bug) => (
                <tr key={bug.id}>
                  <td className="bug-id">{bug.id}</td>
                  <td className="bug-title-cell">
                    <span className="bug-title">{bug.title}</span>
                    {bug.isDuplicate && <span className="duplicate-tag">Duplicate</span>}
                  </td>
                  <td className="bug-env">{bug.environment}</td>
                  <td>
                    <SeverityBadge severity={bug.severity} />
                  </td>
                  <td>
                    <span className={`status-pill status-${bug.status?.toLowerCase().replace(/\s+/g, '-')}`}>
                      {bug.status}
                    </span>
                  </td>
                  <td className="bug-date">{bug.createdAt}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
