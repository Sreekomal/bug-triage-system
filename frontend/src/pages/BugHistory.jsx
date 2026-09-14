import React, { useState } from 'react';
import SeverityBadge from '../components/SeverityBadge.jsx';
import './BugHistory.css';

function BugHistory({ bugs, onNavigate }) {
  const [selectedSeverity, setSelectedSeverity] = useState('ALL');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedBug, setSelectedBug] = useState(null);

  const filteredBugs = bugs.filter((bug) => {
    const matchesSeverity =
      selectedSeverity === 'ALL' ||
      bug.severity?.toUpperCase() === selectedSeverity;

    const matchesSearch =
      searchTerm === '' ||
      bug.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      bug.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      bug.environment.toLowerCase().includes(searchTerm.toLowerCase());

    return matchesSeverity && matchesSearch;
  });

  const severityFilters = ['ALL', 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'];

  return (
    <div className="history-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Bug Triage History</h1>
          <p className="page-subtitle">
            Catalog of all previously reported issues, classified severities, and triage statuses.
          </p>
        </div>
        <button className="primary-action-btn" onClick={() => onNavigate('submit')}>
          <span className="btn-icon">+</span> Report New Bug
        </button>
      </div>

      {/* Control Bar: Search and Severity Filters */}
      <div className="history-controls">
        <div className="search-box">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            className="search-input"
            placeholder="Search by Bug ID, title, environment..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
          {searchTerm && (
            <button className="clear-search-btn" onClick={() => setSearchTerm('')}>
              ✕
            </button>
          )}
        </div>

        <div className="filter-chips">
          {severityFilters.map((filter) => (
            <button
              key={filter}
              className={`filter-chip ${selectedSeverity === filter ? 'active' : ''}`}
              onClick={() => setSelectedSeverity(filter)}
            >
              {filter}
              <span className="filter-count">
                {filter === 'ALL'
                  ? bugs.length
                  : bugs.filter((b) => b.severity?.toUpperCase() === filter).length}
              </span>
            </button>
          ))}
        </div>
      </div>

      {/* Main Table */}
      <div className="history-table-card">
        <div className="table-wrapper">
          <table className="history-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Bug Title</th>
                <th>Environment</th>
                <th>Severity</th>
                <th>Status</th>
                <th>Reported Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredBugs.length > 0 ? (
                filteredBugs.map((bug) => (
                  <tr key={bug.id} className={selectedBug?.id === bug.id ? 'row-selected' : ''}>
                    <td className="bug-id">{bug.id}</td>
                    <td className="bug-main-col">
                      <div className="bug-title-line">
                        <span className="bug-title-text">{bug.title}</span>
                        {bug.isDuplicate && (
                          <span className="duplicate-tag" title="Identified as duplicate issue">
                            Duplicate
                          </span>
                        )}
                      </div>
                      <p className="bug-desc-snippet">{bug.description}</p>
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
                    <td>
                      <button
                        className="details-btn"
                        onClick={() => setSelectedBug(selectedBug?.id === bug.id ? null : bug)}
                      >
                        {selectedBug?.id === bug.id ? 'Close' : 'Details'}
                      </button>
                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td colSpan={7} className="empty-state">
                    No bugs found matching the current search or severity filter.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Selected Bug Detail Modal/Card */}
      {selectedBug && (
        <div className="bug-detail-overlay" onClick={() => setSelectedBug(null)}>
          <div className="bug-detail-modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <div className="modal-title-group">
                <span className="modal-bug-id">{selectedBug.id}</span>
                <h2>{selectedBug.title}</h2>
              </div>
              <button className="modal-close-btn" onClick={() => setSelectedBug(null)}>
                ✕
              </button>
            </div>

            <div className="modal-tags-row">
              <SeverityBadge severity={selectedBug.severity} />
              <span className="modal-pill env-pill">Env: {selectedBug.environment}</span>
              <span className={`status-pill status-${selectedBug.status?.toLowerCase().replace(/\s+/g, '-')}`}>
                Status: {selectedBug.status}
              </span>
              {selectedBug.isDuplicate && <span className="duplicate-tag">Duplicate</span>}
              <span className="modal-pill date-pill">Reported: {selectedBug.createdAt}</span>
            </div>

            <div className="modal-section">
              <h4>Description</h4>
              <p>{selectedBug.description}</p>
            </div>

            {selectedBug.stepsToReproduce && (
              <div className="modal-section">
                <h4>Steps to Reproduce</h4>
                <pre className="modal-pre">{selectedBug.stepsToReproduce}</pre>
              </div>
            )}

            <div className="modal-two-col">
              {selectedBug.expectedResult && (
                <div className="modal-section">
                  <h4>Expected Result</h4>
                  <p>{selectedBug.expectedResult}</p>
                </div>
              )}
              {selectedBug.actualResult && (
                <div className="modal-section">
                  <h4>Actual Result</h4>
                  <p>{selectedBug.actualResult}</p>
                </div>
              )}
            </div>

            <div className="modal-footer">
              <button className="modal-btn secondary" onClick={() => setSelectedBug(null)}>
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default BugHistory;
