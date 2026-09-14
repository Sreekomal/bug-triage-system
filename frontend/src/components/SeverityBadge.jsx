import React from 'react';
import './SeverityBadge.css';

function SeverityBadge({ severity }) {
  const normalized = (severity || 'low').toLowerCase();

  return (
    <span className={`severity-badge severity-${normalized}`}>
      <span className="badge-dot" />
      {severity}
    </span>
  );
}

export default SeverityBadge;
