import React, { useState } from 'react';
import SeverityBadge from '../components/SeverityBadge.jsx';
import { analyzeBug } from '../services/api.js';
import './SubmitBug.css';

function SubmitBug({ onAddBug, onNavigate }) {
  const [formData, setFormData] = useState({
    title: '',
    environment: 'Production',
    description: '',
    stepsToReproduce: '',
    expectedResult: '',
    actualResult: ''
  });

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errors, setErrors] = useState({});

  const validateForm = () => {
    const newErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Bug Title is required.';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Bug Description is required.';
    }

    if (!formData.environment.trim()) {
      newErrors.environment = 'Environment is required.';
    }

    if (Object.keys(newErrors).length > 0) {
      newErrors.general = 'Please fill in all required fields marked with an asterisk (*).';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));

    // Clear specific field error on user edit
    if (errors[name] || errors.general) {
      setErrors((prev) => {
        const updated = { ...prev };
        delete updated[name];
        delete updated.general;
        return updated;
      });
    }
  };

  const handleFillSample = () => {
    setFormData({
      title: 'Crash in authentication pipeline on concurrent token refresh',
      environment: 'Production',
      description: 'Multiple simultaneous API requests with an expired token trigger a race condition in the auth interceptor, resulting in an unhandled Promise rejection and application lockup.',
      stepsToReproduce: '1. Log into portal with test account\n2. Trigger 5 parallel dashboard queries immediately before token expiry (at 59m 50s)\n3. Observe client crash in browser console',
      expectedResult: 'First request initiates single token exchange, pending requests await resolution cleanly.',
      actualResult: 'Multiple exchange requests sent simultaneously, causing 401 unauthorized and frozen UI.'
    });
    setAnalysisResult(null);
    setErrors({});
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsAnalyzing(true);
    setAnalysisResult(null);

    try {
      // Calls centralized service layer (prepared for FastAPI integration)
      const analyzedBug = await analyzeBug(formData);

      setAnalysisResult(analyzedBug);

      // Update session bug state in App so Dashboard and Bug History stay in sync
      if (onAddBug) {
        onAddBug(analyzedBug);
      }
    } catch (err) {
      setErrors({
        general: err.message || 'An error occurred while analyzing the bug report. Please try again.'
      });
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleReset = () => {
    setFormData({
      title: '',
      environment: 'Production',
      description: '',
      stepsToReproduce: '',
      expectedResult: '',
      actualResult: ''
    });
    setAnalysisResult(null);
    setErrors({});
  };

  return (
    <div className="submit-page">
      <div className="page-header">
        <div>
          <h1 className="page-title">Submit Bug for Triage</h1>
          <p className="page-subtitle">
            Provide issue details below. The AI analysis engine will classify severity, assess duplicate probability, and recommend routing.
          </p>
        </div>
        <button
          type="button"
          className="secondary-btn"
          onClick={handleFillSample}
          disabled={isAnalyzing}
        >
          ✨ Fill Demo Sample
        </button>
      </div>

      <div className="submit-grid">
        <form className="bug-form" onSubmit={handleAnalyze} noValidate>
          {errors.general && (
            <div className="form-error-banner">
              <span>⚠️</span>
              <span>{errors.general}</span>
            </div>
          )}

          <div className="form-row two-col">
            <div className="form-group">
              <label htmlFor="title">
                Bug Title <span className="required">*</span>
              </label>
              <input
                id="title"
                name="title"
                type="text"
                className={`form-input ${errors.title ? 'input-error' : ''}`}
                placeholder="e.g., Memory leak in background worker"
                value={formData.title}
                onChange={handleChange}
                disabled={isAnalyzing}
              />
              {errors.title && <span className="field-error-msg">{errors.title}</span>}
            </div>

            <div className="form-group">
              <label htmlFor="environment">
                Environment <span className="required">*</span>
              </label>
              <select
                id="environment"
                name="environment"
                className={`form-select ${errors.environment ? 'input-error' : ''}`}
                value={formData.environment}
                onChange={handleChange}
                disabled={isAnalyzing}
              >
                <option value="Production">Production</option>
                <option value="Staging">Staging</option>
                <option value="QA">QA</option>
                <option value="Development">Development</option>
              </select>
              {errors.environment && <span className="field-error-msg">{errors.environment}</span>}
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="description">
              Bug Description <span className="required">*</span>
            </label>
            <textarea
              id="description"
              name="description"
              rows={3}
              className={`form-textarea ${errors.description ? 'input-error' : ''}`}
              placeholder="Detailed description of what is failing, impact, and observed behavior..."
              value={formData.description}
              onChange={handleChange}
              disabled={isAnalyzing}
            />
            {errors.description && <span className="field-error-msg">{errors.description}</span>}
          </div>

          <div className="form-group">
            <label htmlFor="stepsToReproduce">Steps to Reproduce</label>
            <textarea
              id="stepsToReproduce"
              name="stepsToReproduce"
              rows={3}
              className="form-textarea"
              placeholder="1. Step one&#10;2. Step two&#10;3. Observed error"
              value={formData.stepsToReproduce}
              onChange={handleChange}
              disabled={isAnalyzing}
            />
          </div>

          <div className="form-row two-col">
            <div className="form-group">
              <label htmlFor="expectedResult">Expected Result</label>
              <textarea
                id="expectedResult"
                name="expectedResult"
                rows={2}
                className="form-textarea"
                placeholder="What should have happened..."
                value={formData.expectedResult}
                onChange={handleChange}
                disabled={isAnalyzing}
              />
            </div>

            <div className="form-group">
              <label htmlFor="actualResult">Actual Result</label>
              <textarea
                id="actualResult"
                name="actualResult"
                rows={2}
                className="form-textarea"
                placeholder="What actually occurred..."
                value={formData.actualResult}
                onChange={handleChange}
                disabled={isAnalyzing}
              />
            </div>
          </div>

          <div className="form-actions">
            <button
              type="submit"
              className="analyze-btn"
              disabled={isAnalyzing}
            >
              {isAnalyzing ? (
                <>
                  <span className="spinner" /> Analyzing...
                </>
              ) : (
                <>
                  <span className="btn-icon">⚡</span> Analyze Bug
                </>
              )}
            </button>
            <button
              type="button"
              className="reset-btn"
              onClick={handleReset}
              disabled={isAnalyzing}
            >
              Clear
            </button>
          </div>
        </form>

        {/* AI Analysis Preview Card */}
        <div className="analysis-sidebar">
          {analysisResult ? (
            <div className="result-card">
              <div className="result-card-header">
                <span className="result-chip">AI Analysis Complete</span>
                <span className="result-id">{analysisResult.id}</span>
              </div>

              <h3 className="result-title">Triage Classification</h3>

              <div className="result-metric-box">
                <div className="metric-item">
                  <span className="metric-label">Predicted Severity</span>
                  <div className="metric-value">
                    <SeverityBadge severity={analysisResult.severity} />
                  </div>
                </div>
                <div className="metric-item">
                  <span className="metric-label">Confidence Score</span>
                  <span className="confidence-score">{analysisResult.confidence}%</span>
                </div>
              </div>

              <div className="result-details-list">
                <div className="detail-row">
                  <span className="detail-label">Recommended Component</span>
                  <span className="detail-val">{analysisResult.component}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Duplicate Similarity</span>
                  <span className="detail-val">{analysisResult.duplicateProbability}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Target Environment</span>
                  <span className="detail-val">{analysisResult.environment}</span>
                </div>
              </div>

              <div className="result-success-note">
                ✓ Successfully analyzed and added to local Bug History.
              </div>

              <button
                type="button"
                className="view-history-btn"
                onClick={() => onNavigate('history')}
              >
                View in Bug History →
              </button>
            </div>
          ) : (
            <div className="placeholder-card">
              <div className="placeholder-icon">🤖</div>
              <h3 className="placeholder-title">AI Triage Ready</h3>
              <p className="placeholder-desc">
                Fill in the bug details and click <strong>Analyze Bug</strong> to view the automated severity prediction, confidence evaluation, and component recommendation.
              </p>
              <div className="features-list">
                <div className="feature-item">✓ Natural Language Severity Scoring</div>
                <div className="feature-item">✓ Redundant Bug / Duplicate Detection</div>
                <div className="feature-item">✓ Automatic Routing Recommendation</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default SubmitBug;
