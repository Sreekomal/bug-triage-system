import React, { useState } from 'react';
import Navbar from './components/Navbar.jsx';
import Dashboard from './pages/Dashboard.jsx';
import SubmitBug from './pages/SubmitBug.jsx';
import BugHistory from './pages/BugHistory.jsx';
import { initialBugs } from './data/mockBugs.js';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [bugs, setBugs] = useState(initialBugs);

  const handleAddBug = (newBug) => {
    setBugs((prev) => [newBug, ...prev]);
  };

  return (
    <div className="app-root">
      <Navbar activeTab={activeTab} onSelectTab={setActiveTab} />

      <main className="main-content">
        <div className="content-container">
          {activeTab === 'dashboard' && (
            <Dashboard bugs={bugs} onNavigate={setActiveTab} />
          )}

          {activeTab === 'submit' && (
            <SubmitBug onAddBug={handleAddBug} onNavigate={setActiveTab} />
          )}

          {activeTab === 'history' && (
            <BugHistory bugs={bugs} onNavigate={setActiveTab} />
          )}
        </div>
      </main>

      <footer className="app-footer">
        <div className="footer-inner">
          <p>
            <strong>AI Bug Triage System</strong> • Automated Bug Classification & Defect Triage
          </p>
          <p className="footer-note">Frontend UI Prototype • React + Vite</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
