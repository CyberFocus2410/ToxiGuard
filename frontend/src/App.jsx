import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import PredictionForm from './components/PredictionForm';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <Router>
      <div className="app-container">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<PredictionForm />} />
            <Route path="/dashboard" element={<Dashboard />} />
          </Routes>
        </main>
        
        <footer style={{ borderTop: '1px solid var(--glass-border)', padding: '3rem 0', marginTop: 'auto', color: 'var(--text-secondary)', fontSize: '0.95rem', textAlign: 'center', background: 'rgba(30, 41, 59, 0.4)' }}>
          <div className="container">
            <p style={{ fontWeight: '600' }}>&copy; 2026 ToxiGuard AI Platform. Molecular Security & Toxicity Surveillance.</p>
            <div style={{ marginTop: '0.75rem', display: 'flex', gap: '1.5rem', justifyContent: 'center', opacity: 0.7, fontSize: '0.85rem' }}>
               <span>v1.0.4-LATEST</span>
               <span>Tox21 High-Throughput Dataset</span>
               <span>SHAP Explainable Intelligence</span>
            </div>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
