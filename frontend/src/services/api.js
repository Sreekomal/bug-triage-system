/**
 * API Service Layer for AI Bug Triage System
 *
 * This file serves as the centralized communication bridge between the React frontend
 * and the future FastAPI backend (e.g., http://localhost:8000/api).
 *
 * Currently, it simulates the AI triage analysis asynchronously using mock business logic.
 * When connecting to the real FastAPI backend, simply uncomment the fetch implementations below.
 */

// Base URL for backend API (configurable via Vite environment variables)
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

/**
 * Analyzes a bug report using the AI Triage model.
 *
 * FUTURE FASTAPI INTEGRATION POINT:
 * POST /api/triage/analyze
 *
 * @param {Object} bugData - { title, description, stepsToReproduce, expectedResult, actualResult, environment }
 * @returns {Promise<Object>} Triaged bug object with predicted severity, confidence, component, and duplicate status.
 */
export async function analyzeBug(bugData) {
  /*
  // --- UNCOMMENT FOR REAL FASTAPI BACKEND ---
  const response = await fetch(`${API_BASE_URL}/triage/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(bugData),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Analysis failed with status ${response.status}`);
  }

  return await response.json();
  // ------------------------------------------
  */

  // Simulated AI Triage Service (Mock implementation)
  return new Promise((resolve) => {
    setTimeout(() => {
      const text = `${bugData.title} ${bugData.description}`.toLowerCase();
      let predictedSeverity = 'High';
      let confidence = 94.8;
      let component = 'Authentication / Security';
      let duplicateProbability = '12%';
      let isDuplicate = false;

      if (
        text.includes('crash') ||
        text.includes('memory') ||
        text.includes('out of memory') ||
        text.includes('fatal') ||
        text.includes('leak')
      ) {
        predictedSeverity = 'Critical';
        confidence = 97.4;
        component = 'Core Runtime / Stability';
        duplicateProbability = '8%';
      } else if (
        text.includes('align') ||
        text.includes('css') ||
        text.includes('color') ||
        text.includes('typo') ||
        text.includes('padding')
      ) {
        predictedSeverity = 'Low';
        confidence = 91.2;
        component = 'Frontend UI';
        duplicateProbability = '4%';
      } else if (text.includes('timeout') || text.includes('latency') || text.includes('slow')) {
        predictedSeverity = 'High';
        confidence = 93.6;
        component = 'Performance / Network';
        duplicateProbability = '15%';
      }

      // Check for duplicate keyword demo
      if (text.includes('duplicate')) {
        isDuplicate = true;
        duplicateProbability = '88%';
      }

      // Structured schema aligned with future FastAPI Pydantic schema
      const analyzedBug = {
        id: `BUG-${Math.floor(1000 + Math.random() * 9000)}`,
        title: bugData.title.trim(),
        description: bugData.description.trim(),
        stepsToReproduce: bugData.stepsToReproduce ? bugData.stepsToReproduce.trim() : '',
        expectedResult: bugData.expectedResult ? bugData.expectedResult.trim() : '',
        actualResult: bugData.actualResult ? bugData.actualResult.trim() : '',
        environment: bugData.environment || 'Production',
        // Triage classification payload
        severity: predictedSeverity,
        confidence: confidence,
        component: component,
        duplicateProbability: duplicateProbability,
        isDuplicate: isDuplicate,
        status: 'Open',
        createdAt: new Date().toISOString().split('T')[0]
      };

      resolve(analyzedBug);
    }, 700);
  });
}

/**
 * Placeholder: Fetch all bug records from backend.
 * Future Endpoint: GET /api/bugs
 */
export async function getBugs() {
  /*
  const response = await fetch(`${API_BASE_URL}/bugs`);
  if (!response.ok) throw new Error('Failed to fetch bugs');
  return await response.json();
  */
  return Promise.resolve([]);
}

/**
 * Placeholder: Fetch a single bug by ID.
 * Future Endpoint: GET /api/bugs/{id}
 */
export async function getBugById(id) {
  /*
  const response = await fetch(`${API_BASE_URL}/bugs/${id}`);
  if (!response.ok) throw new Error(`Failed to fetch bug ${id}`);
  return await response.json();
  */
  return Promise.resolve(null);
}
