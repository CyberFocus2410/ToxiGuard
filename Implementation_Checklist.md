# CodeCure Implementation Checklist & Code Templates

## QUICK START CHECKLIST

### ✅ Pre-Hackathon Setup (Do This Now)
- [ ] Create Anthropic API account → Get API key
- [ ] Create Antigravity account → Familiarize with interface
- [ ] Install required tools locally:
  ```bash
  pip install scikit-learn xgboost shap rdkit pandas numpy
  pip install requests flask
  ```
- [ ] Clone/fork basic React template
- [ ] Download Tox21 dataset from Kaggle

---

## CLAUDE API - ML PIPELINE GENERATION

### Template Prompt 1: Complete ML Pipeline

```
Please generate production-ready Python code for a drug toxicity prediction system.

Requirements:
1. Load Tox21 dataset (assume CSV file: "tox21_data.csv")
2. Compute 20+ molecular descriptors using RDKit
3. Train XGBoost classifier
4. Calculate SHAP values for interpretability
5. Predict toxicity + return risk factors
6. Calculate and report: accuracy, F1 score, AUC-ROC

Dataset columns:
- SMILES: Chemical structure as SMILES string
- Toxicity: Binary (0 = non-toxic, 1 = toxic)

Output requirements:
- save_model(model, "toxicity_model.pkl")
- load_model("toxicity_model.pkl") → model
- predict_single(smiles: str) → {prob, factors, confidence}
- evaluate() → {accuracy, f1, auc}

Include:
- Data preprocessing (handle missing values, duplicates)
- 80/20 train-test split
- 5-fold cross-validation
- Feature scaling
- Clear docstrings
```

### Template Code: Antigravity Integration

```python
# ml_pipeline.py
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import shap
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem

class ToxicityPredictor:
    def __init__(self, model_path=None):
        self.model = None
        self.scaler = None
        self.shap_explainer = None
        self.feature_names = self._get_feature_names()
        
        if model_path:
            self.load_model(model_path)
    
    def _get_feature_names(self):
        """All molecular descriptors to compute"""
        return [
            'LogP', 'MolWt', 'NumRotatableBonds', 'NumHDonors',
            'NumHAcceptors', 'NumRings', 'NumAromaticRings', 'TPSA',
            'EState_VSA1', 'EState_VSA2', 'EState_VSA3', 'EState_VSA4',
            'EState_VSA5', 'EState_VSA6', 'LabuteASA', 'PEOE_VSA1',
            'PEOE_VSA2', 'PEOE_VSA3', 'PEOE_VSA4', 'PEOE_VSA5'
        ]
    
    def compute_descriptors(self, smiles):
        """Compute molecular descriptors from SMILES"""
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            raise ValueError(f"Invalid SMILES: {smiles}")
        
        descriptors = {
            'LogP': Descriptors.MolLogP(mol),
            'MolWt': Descriptors.MolWt(mol),
            'NumRotatableBonds': Descriptors.NumRotatableBonds(mol),
            'NumHDonors': Descriptors.NumHDonors(mol),
            'NumHAcceptors': Descriptors.NumHAcceptors(mol),
            'NumRings': Descriptors.RingCount(mol),
            'NumAromaticRings': Descriptors.NumAromaticRings(mol),
            'TPSA': Descriptors.TPSA(mol),
            # ... add rest of descriptors
        }
        return np.array([descriptors[feat] for feat in self.feature_names])
    
    def predict(self, smiles):
        """
        Predict toxicity for a single compound
        
        Returns:
        {
            'toxicity_probability': float (0-1),
            'toxicity_category': 'High'|'Medium'|'Low',
            'risk_factors': [{'feature': str, 'value': float, 'importance': float}],
            'confidence': float
        }
        """
        if not self.model:
            raise RuntimeError("Model not loaded")
        
        # Compute descriptors
        features = self.compute_descriptors(smiles)
        features_scaled = self.scaler.transform([features])
        
        # Get prediction
        prob = self.model.predict_proba(features_scaled)[0][1]
        
        # Get SHAP values for interpretation
        shap_values = self.shap_explainer.shap_values(features_scaled)[0]
        
        # Rank risk factors by absolute SHAP value
        risk_factors = [
            {
                'feature': self.feature_names[i],
                'value': float(features[i]),
                'importance': float(abs(shap_values[i])),
                'contribution': 'increases' if shap_values[i] > 0 else 'decreases'
            }
            for i in range(len(self.feature_names))
        ]
        risk_factors = sorted(risk_factors, key=lambda x: x['importance'], reverse=True)[:5]
        
        # Categorize risk level
        if prob >= 0.7:
            category = 'High'
        elif prob >= 0.4:
            category = 'Medium'
        else:
            category = 'Low'
        
        return {
            'toxicity_probability': float(prob),
            'toxicity_category': category,
            'risk_factors': risk_factors,
            'confidence': float(max(self.model.predict_proba(features_scaled)[0]))
        }
    
    def save_model(self, path):
        """Save trained model"""
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'explainer': self.shap_explainer
            }, f)
    
    def load_model(self, path):
        """Load saved model"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.shap_explainer = data['explainer']

# Usage in Antigravity
def predict_toxicity_api(smiles):
    predictor = ToxicityPredictor("models/toxicity_model.pkl")
    result = predictor.predict(smiles)
    return result
```

---

## ANTIGRAVITY BACKEND SETUP

### Database Schema (SQL)

```sql
-- Predictions table
CREATE TABLE predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),
    smiles TEXT NOT NULL,
    toxicity_prob FLOAT NOT NULL,
    toxicity_category VARCHAR(20),
    risk_factors JSONB,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Model metadata
CREATE TABLE model_metadata (
    id SERIAL PRIMARY KEY,
    model_version VARCHAR(50),
    accuracy FLOAT,
    f1_score FLOAT,
    auc_roc FLOAT,
    training_date TIMESTAMP,
    num_training_samples INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Feature importance
CREATE TABLE feature_importance (
    id SERIAL PRIMARY KEY,
    model_version VARCHAR(50),
    feature_name VARCHAR(100),
    importance_score FLOAT,
    rank INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_predictions_user ON predictions(user_id);
CREATE INDEX idx_predictions_created ON predictions(created_at);
```

### API Endpoint Configuration

In Antigravity Visual Builder:

**Endpoint 1: POST /api/predict**
```
Input: {
  "smiles": "CCO",
  "user_id": "user123"
}

Workflow:
1. Validate SMILES format
2. Call Python function: predict_toxicity_api(smiles)
3. Store result in predictions table
4. Call Claude API for interpretation
5. Return response

Output: {
  "id": "uuid",
  "toxicity_probability": 0.25,
  "toxicity_category": "Low",
  "risk_factors": [
    {"feature": "LogP", "value": 1.2, "importance": 0.35, "contribution": "increases"}
  ],
  "interpretation": "This compound has low toxicity risk...",
  "confidence": 0.92
}
```

**Endpoint 2: GET /api/predictions/:user_id**
```
Query database for all predictions by user
Return: [{ prediction1 }, { prediction2 }, ...]
```

**Endpoint 3: GET /api/model-stats**
```
Query model_metadata table (latest version)
Return: {
  "accuracy": 0.87,
  "f1_score": 0.84,
  "auc_roc": 0.91,
  "training_date": "2024-04-03"
}
```

**Endpoint 4: GET /api/feature-importance**
```
Query feature_importance table
Return top 10 features:
[
  {"rank": 1, "feature": "LogP", "importance": 0.185},
  {"rank": 2, "feature": "NumHDonors", "importance": 0.142},
  ...
]
```

---

## FRONTEND - REACT COMPONENTS

### Component 1: Prediction Form

```jsx
// components/PredictionForm.jsx
import React, { useState } from 'react';
import axios from 'axios';
import './PredictionForm.css';

export default function PredictionForm() {
  const [smiles, setSmiles] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handlePredict = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/api/predict`,
        { 
          smiles: smiles,
          user_id: 'demo_user' // Replace with actual user auth
        }
      );
      setResult(response.data);
    } catch (err) {
      if (err.response?.status === 400) {
        setError('Invalid SMILES format. Example: CCO (ethanol)');
      } else {
        setError('Prediction failed. Please try again.');
      }
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-form-container">
      <div className="form-section">
        <h2>Drug Toxicity Predictor</h2>
        <form onSubmit={handlePredict}>
          <div className="form-group">
            <label htmlFor="smiles">Enter SMILES String:</label>
            <input
              id="smiles"
              type="text"
              placeholder="e.g., CCO, CC(=O)OC1=CC=CC=C1C(=O)O"
              value={smiles}
              onChange={(e) => setSmiles(e.target.value)}
              disabled={loading}
            />
            <small>Don't know SMILES? Use an online SMILES generator</small>
          </div>
          <button type="submit" disabled={loading || !smiles.trim()}>
            {loading ? 'Analyzing...' : 'Predict Toxicity'}
          </button>
        </form>
        {error && <p className="error-message">{error}</p>}
      </div>

      {result && (
        <div className="results-section">
          <div className={`toxicity-score ${result.toxicity_category.toLowerCase()}`}>
            <h3>Toxicity Score</h3>
            <div className="score-display">
              {(result.toxicity_probability * 100).toFixed(1)}%
            </div>
            <div className="risk-level">{result.toxicity_category} Risk</div>
            <div className="confidence">
              Confidence: {(result.confidence * 100).toFixed(1)}%
            </div>
          </div>

          <div className="interpretation-box">
            <h4>Biological Interpretation</h4>
            <p>{result.interpretation}</p>
          </div>

          <div className="risk-factors-section">
            <h4>Top Risk Factors:</h4>
            <table className="risk-factors-table">
              <thead>
                <tr>
                  <th>Feature</th>
                  <th>Value</th>
                  <th>Importance</th>
                  <th>Effect</th>
                </tr>
              </thead>
              <tbody>
                {result.risk_factors.map((factor, idx) => (
                  <tr key={idx}>
                    <td>{factor.feature}</td>
                    <td>{factor.value.toFixed(2)}</td>
                    <td>
                      <div className="importance-bar">
                        <div 
                          className="importance-fill"
                          style={{ width: `${factor.importance * 100}%` }}
                        ></div>
                      </div>
                      {(factor.importance * 100).toFixed(1)}%
                    </td>
                    <td className={factor.contribution}>
                      {factor.contribution}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
```

### Component 2: Dashboard

```jsx
// components/Dashboard.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import './Dashboard.css';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [features, setFeatures] = useState([]);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, featuresRes, predictionsRes] = await Promise.all([
          axios.get(`${process.env.REACT_APP_API_URL}/api/model-stats`),
          axios.get(`${process.env.REACT_APP_API_URL}/api/feature-importance`),
          axios.get(`${process.env.REACT_APP_API_URL}/api/predictions/demo_user`)
        ]);
        
        setStats(statsRes.data);
        setFeatures(featuresRes.data);
        setPredictions(predictionsRes.data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading dashboard...</div>;

  return (
    <div className="dashboard-container">
      <h1>Toxicity Prediction Dashboard</h1>

      {/* Model Stats */}
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Model Accuracy</h3>
          <p className="stat-value">{(stats?.accuracy * 100).toFixed(1)}%</p>
        </div>
        <div className="stat-card">
          <h3>F1 Score</h3>
          <p className="stat-value">{stats?.f1_score.toFixed(3)}</p>
        </div>
        <div className="stat-card">
          <h3>AUC-ROC</h3>
          <p className="stat-value">{stats?.auc_roc.toFixed(3)}</p>
        </div>
      </div>

      {/* Feature Importance Chart */}
      <div className="chart-section">
        <h2>Top 10 Important Features</h2>
        <BarChart width={800} height={400} data={features}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="feature_name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="importance_score" fill="#8884d8" />
        </BarChart>
      </div>

      {/* Recent Predictions */}
      <div className="predictions-section">
        <h2>Recent Predictions</h2>
        <table className="predictions-table">
          <thead>
            <tr>
              <th>SMILES</th>
              <th>Toxicity %</th>
              <th>Risk Level</th>
              <th>Date</th>
            </tr>
          </thead>
          <tbody>
            {predictions.map(pred => (
              <tr key={pred.id}>
                <td className="smiles-cell" title={pred.smiles}>
                  {pred.smiles.substring(0, 30)}...
                </td>
                <td>{(pred.toxicity_prob * 100).toFixed(1)}</td>
                <td>
                  <span className={`risk-badge ${pred.toxicity_category.toLowerCase()}`}>
                    {pred.toxicity_category}
                  </span>
                </td>
                <td>{new Date(pred.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
```

### CSS Styling

```css
/* PredictionForm.css */
.prediction-form-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 2rem;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.form-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
  border-radius: 12px;
  color: white;
  margin-bottom: 2rem;
}

.form-section h2 {
  margin: 0 0 1.5rem 0;
  font-size: 24px;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-family: 'Monaco', 'Courier New', monospace;
}

button {
  width: 100%;
  padding: 12px;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  font-size: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.toxicity-score {
  background: white;
  padding: 2rem;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 2rem;
  border-left: 6px solid;
}

.toxicity-score.high { border-left-color: #ff6b6b; }
.toxicity-score.medium { border-left-color: #ffa94d; }
.toxicity-score.low { border-left-color: #51cf66; }

.score-display {
  font-size: 48px;
  font-weight: 700;
  color: #333;
  margin: 1rem 0;
}

.risk-level {
  font-size: 20px;
  font-weight: 600;
  color: #666;
}

.confidence {
  margin-top: 1rem;
  font-size: 14px;
  color: #999;
}

.risk-factors-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.risk-factors-table th,
.risk-factors-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.risk-factors-table th {
  background: #f5f5f5;
  font-weight: 600;
  color: #333;
}

.importance-bar {
  width: 100px;
  height: 20px;
  background: #eee;
  border-radius: 4px;
  overflow: hidden;
  display: inline-block;
  margin-right: 8px;
}

.importance-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
}

.error-message {
  color: #ff6b6b;
  margin-top: 1rem;
  padding: 12px;
  background: #ffe0e0;
  border-radius: 6px;
}
```

---

## Environment Configuration

### .env file (Frontend)
```
REACT_APP_API_URL=https://your-antigravity-backend.com
REACT_APP_VERSION=1.0.0
```

### .env file (Backend - if using local development)
```
ANTHROPIC_API_KEY=sk-ant-...
DATABASE_URL=postgresql://user:password@localhost:5432/codecure
ML_MODEL_PATH=./models/toxicity_model.pkl
```

---

## Testing Checklist

### Unit Tests
```python
# test_ml_pipeline.py
def test_predict_aspirin():
    predictor = ToxicityPredictor("models/toxicity_model.pkl")
    result = predictor.predict("CC(=O)OC1=CC=CC=C1C(=O)O")  # Aspirin
    assert 0 <= result['toxicity_probability'] <= 1
    assert len(result['risk_factors']) == 5
    assert result['toxicity_category'] in ['High', 'Medium', 'Low']

def test_invalid_smiles():
    predictor = ToxicityPredictor("models/toxicity_model.pkl")
    with pytest.raises(ValueError):
        predictor.predict("INVALID_SMILES")
```

### Integration Tests
```javascript
// __tests__/api.test.js
describe('Prediction API', () => {
  test('POST /api/predict returns valid response', async () => {
    const response = await axios.post('/api/predict', {
      smiles: 'CCO',
      user_id: 'test_user'
    });
    
    expect(response.status).toBe(200);
    expect(response.data).toHaveProperty('toxicity_probability');
    expect(response.data).toHaveProperty('risk_factors');
  });
});
```

---

## Final Submission Checklist

- [ ] Model achieves 85%+ accuracy
- [ ] All 4 API endpoints working
- [ ] Frontend loads within 3 seconds
- [ ] Predictions return in <2 seconds
- [ ] Database stores results
- [ ] Claude API generates interpretations
- [ ] Dashboard shows correct metrics
- [ ] README.md complete with examples
- [ ] GitHub repo clean and documented
- [ ] Demo script prepared (5 test cases)
- [ ] Presentation slides ready
- [ ] Deployed and tested end-to-end

