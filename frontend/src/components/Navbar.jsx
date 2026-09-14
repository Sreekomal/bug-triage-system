import React from 'react';
import './Navbar.css';

function Navbar({ activeTab, onSelectTab }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'submit', label: 'Submit Bug' },
    { id: 'history', label: 'Bug History' }
  ];

  return (
    <header className="navbar">
      <div className="navbar-inner">
        <div className="navbar-brand" onClick={() => onSelectTab('dashboard')}>
          <div className="brand-logo">
            <span className="brand-icon">⚡</span>
          </div>
          <div className="brand-text">
            <span className="brand-title">AI Bug Triage System</span>
            <span className="brand-tag">Intelligent Classifier</span>
          </div>
        </div>

        <nav className="navbar-nav">
          {navItems.map((item) => (
            <button
              key={item.id}
              className={`nav-button ${activeTab === item.id ? 'active' : ''}`}
              onClick={() => onSelectTab(item.id)}
            >
              {item.label}
              {activeTab === item.id && <span className="nav-indicator" />}
            </button>
          ))}
        </nav>
      </div>
    </header>
  );
}

export default Navbar;
