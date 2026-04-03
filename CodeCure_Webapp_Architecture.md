# CodeCure Drug Toxicity Prediction - Complete Webapp Guide
## Building with Claude AI Studio + Antigravity

---

## Overview: Your Complete Tech Stack

You'll build a **production-ready, full-stack application** that combines:
- **Claude API** → ML model generation + feature engineering + interpretation
- **Antigravity** → Visual backend, database, API routing
- **Frontend** → React/Vue dashboard for predictions
- **Database** → Store predictions, user data, model metadata

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│              FRONTEND (React/Vue.js)                    │
│  - Input: SMILES string or molecule structure          │
│  - Display: Toxicity prediction + Feature importance    │
│  - Dashboard: Historical predictions, trends            │
└──────────────────┬──────────────────────────────────────┘
                   │ API Calls
                   ▼
┌─────────────────────────────────────────────────────────┐
│         ANTIGRAVITY BACKEND (No-Code Logic)             │
│  - REST API endpoints                                   │
│  - Database connections (PostgreSQL/MongoDB)            │
│  - Trigger Python ML pipeline execution                 │
│  - Return results to frontend                           │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
               ▼                          ▼
    ┌──────────────────┐      ┌──────────────────┐
    │  CLAUDE API      │      │  PYTHON ML CODE  │
    │  - Code gen      │      │  - XGBoost model │
    │  - Explanation   │      │  - SHAP analysis │
    │  - Insights      │      │  - Predictions   │
    └──────────────────┘      └──────────────────┘
               │                          │
               └──────────────┬───────────┘
                              │
                              ▼
                   ┌──────────────────────┐
                   │  DATABASE (Antigravity) │
                   │  - Predictions        │
                   │  - Model performance  │
                   │  - User data          │
                   └──────────────────────┘
```

---

## PHASE 1: Setup & Project Structure (Day 1 - Morning)

### Step 1.1: Create Antigravity Backend
1. Sign up at **antigravity.dev**
2. Create a new project: "CodeCure-ToxPredictor"
3. Set up database tables:
   - **Predictions** table:
     - `id` (UUID, primary key)
     - `smiles` (text)
     - `toxicity_prob` (float)
     - `risk_factors` (JSON array)
     - `similar_compounds` (JSON array)
     - `created_at` (timestamp)
   
   - **Model_Metadata** table:
     - `model_version` (string)
     - `accuracy` (float)
     - `f1_score` (float)
     - `training_date` (timestamp)
   
   - **Feature_Importance** table:
     - `feature_name` (text)
     - `importance_score` (float)
     - `rank` (integer)

### Step 1.2: Create API Endpoints in Antigravity
Build these REST endpoints:
- `POST /predict` → receives SMILES, calls ML pipeline, returns prediction
- `GET /predictions/:user_id` → fetch user's prediction history
- `GET /model-stats` → fetch model accuracy, F1 score
- `GET /feature-importance` → fetch top 10 important features

### Step 1.3: Prepare Claude API Integration
Generate your API key from **api.anthropic.com**

Use Claude for:
- **Code generation**: Generating Python ML code
- **Feature engineering**: Suggesting molecular descriptors
- **Result interpretation**: Converting predictions to biological insights

---

## PHASE 2: ML Pipeline Development (Day 1 - Afternoon)

### Step 2.1: Use Claude API to Generate ML Pipeline

**Prompt to Claude:**
```
I'm building a drug toxicity prediction model for a hackathon using the Tox21 dataset.
Generate production-ready Python code for:

1. Load Tox21 dataset from Kaggle
2. Compute molecular descriptors using RDKit (logP, QED, SAS, TPSA, etc.)
3. Train XGBoost model on toxicity prediction
4. Calculate SHAP values for feature importance
5. Function to predict toxicity for a single SMILES string
6. Return top 5 most important risk factors for the prediction

Include:
- Data preprocessing & handling missing values
- Train/test split (80/20)
- Cross-validation (5-fold)
- Model evaluation metrics (accuracy, F1, AUC-ROC)
- Save model to file for later loading

Output as a Python script that can be run independently.
```

**Claude will generate** a complete pipeline you can:
- Download and test locally
- Upload to Antigravity as a custom code function
- Call via API from your frontend

### Step 2.2: Enhance with Feature Engineering

**Ask Claude:**
```
For the Tox21 dataset, suggest 15 additional molecular descriptors I should compute
that might improve toxicity prediction. For each, explain:
1. The descriptor name
2. Why it's relevant to drug toxicity
3. How to compute it using RDKit

Format as a Python dictionary with RDKit function calls.
```

Claude will provide code like:
```python
descriptors = {
    'LogP': Descriptors.MolLogP,
    'Rotatable_Bonds': Descriptors.NumRotatableBonds,
    'H_Bond_Donors': Descriptors.NumHDonors,
    # ... 12 more
}
```

### Step 2.3: Create Prediction Function

Your ML code needs a function like this:

```python
def predict_toxicity(smiles_string, model, scaler, feature_names):
    """
    Predict toxicity for a single compound
    
    Args:
        smiles_string: SMILES representation of molecule
        model: Trained XGBoost model
        scaler: Fitted StandardScaler
        feature_names: List of computed features
    
    Returns:
        {
            'toxicity_probability': float (0-1),
            'toxicity_category': 'High'|'Medium'|'Low',
            'risk_factors': [
                {'feature': 'LogP', 'value': 3.2, 'importance': 0.15},
                ...
            ],
            'confidence': float (0-1)
        }
    """
```

---

## PHASE 3: Frontend Development (Day 1 - Late Evening / Day 2 - Morning)

### Step 3.1: Create React Component

**Main structure:**
```jsx
// PredictionInterface.jsx
import React, { useState } from 'react';
import axios from 'axios';

export default function PredictionInterface() {
  const [smiles, setSmiles] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const response = await axios.post(
        'https://your-antigravity-api.com/predict',
        { smiles: smiles }
      );
      setResult(response.data);
    } catch (error) {
      console.error('Prediction failed:', error);
    }
    setLoading(false);
  };

  return (
    <div className="prediction-container">
      <h1>Drug Toxicity Predictor</h1>
      
      {/* Input Section */}
      <div className="input-section">
        <input
          type="text"
          placeholder="Enter SMILES string (e.g., CCO for ethanol)"
          value={smiles}
          onChange={(e) => setSmiles(e.target.value)}
        />
        <button onClick={handlePredict} disabled={loading}>
          {loading ? 'Predicting...' : 'Predict Toxicity'}
        </button>
      </div>

      {/* Results Section */}
      {result && (
        <div className="results-section">
          <div className="toxicity-score">
            <h2>Toxicity Score: {(result.toxicity_probability * 100).toFixed(1)}%</h2>
            <div className={`risk-level ${result.toxicity_category.toLowerCase()}`}>
              Risk Level: {result.toxicity_category}
            </div>
          </div>

          {/* Feature Importance */}
          <div className="feature-importance">
            <h3>Top Risk Factors:</h3>
            <ul>
              {result.risk_factors.map((factor, i) => (
                <li key={i}>
                  {factor.feature}: {factor.value.toFixed(2)} 
                  (importance: {(factor.importance * 100).toFixed(1)}%)
                </li>
              ))}
            </ul>
          </div>

          {/* Visualization */}
          <div className="chart">
            <FeatureImportanceChart data={result.risk_factors} />
          </div>
        </div>
      )}
    </div>
  );
}
```

### Step 3.2: Create Dashboard Component

```jsx
// Dashboard.jsx
import React, { useEffect, useState } from 'react';
import axios from 'axios';

export default function Dashboard() {
  const [predictions, setPredictions] = useState([]);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // Fetch user's prediction history
    axios.get('/api/predictions/user123')
      .then(res => setPredictions(res.data))
      .catch(err => console.error(err));

    // Fetch model statistics
    axios.get('/api/model-stats')
      .then(res => setStats(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="dashboard">
      <h1>Toxicity Prediction Dashboard</h1>
      
      {/* Model Stats */}
      <div className="stats-card">
        <h3>Model Performance</h3>
        <p>Accuracy: {stats?.accuracy.toFixed(2)}%</p>
        <p>F1 Score: {stats?.f1_score.toFixed(3)}</p>
      </div>

      {/* Prediction History */}
      <div className="history-card">
        <h3>Recent Predictions</h3>
        <table>
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
                <td>{pred.smiles}</td>
                <td>{(pred.toxicity_prob * 100).toFixed(1)}</td>
                <td>{pred.risk_level}</td>
                <td>{new Date(pred.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Feature Importance */}
      <div className="feature-card">
        <h3>Most Important Features (Global)</h3>
        <FeatureImportanceChart data={stats?.top_features} />
      </div>
    </div>
  );
}
```

### Step 3.3: Add Visualizations

Use **Chart.js** or **Recharts** for:
- Feature importance bar charts
- Toxicity prediction distribution
- Model accuracy metrics
- Prediction history timeline

```jsx
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

function FeatureImportanceChart({ data }) {
  return (
    <BarChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="feature" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="importance" fill="#8884d8" />
    </BarChart>
  );
}
```

---

## PHASE 4: Integration Setup (Day 2 - Afternoon)

### Step 4.1: Antigravity API Endpoint Configuration

In Antigravity, create a `POST /predict` endpoint that:

```
1. Receives: { smiles: "CCO" }
2. Validates SMILES format
3. Triggers Python script (your ML pipeline)
4. Stores result in Predictions table
5. Returns: { toxicity_prob, risk_factors, confidence }
```

**Antigravity Workflow (Visual Builder):**
1. Create a "Predict" workflow
2. Add input: SMILES string
3. Add action: Execute Python script
   - Upload your ML code as a custom function
   - Pass SMILES to the function
   - Get back predictions
4. Add action: Save to database
5. Return response to frontend

### Step 4.2: Use Claude API for Generating Interpretation

In your Antigravity backend, after getting predictions:

```python
import anthropic

def generate_interpretation(prediction_result):
    """
    Use Claude to explain the toxicity prediction in biological terms
    """
    client = anthropic.Anthropic(api_key="your-api-key")
    
    prompt = f"""
    A drug toxicity prediction model analyzed the compound {prediction_result['smiles']}.
    
    Results:
    - Predicted toxicity: {prediction_result['toxicity_prob']*100:.1f}%
    - Top risk factors: {', '.join([f'{f[0]}' for f in prediction_result['risk_factors'][:3]])}
    
    Explain in simple biological terms:
    1. Why this compound might be toxic
    2. Which molecular properties contribute to toxicity
    3. What structural modifications could reduce toxicity
    4. Confidence in the prediction
    
    Keep it under 150 words, suitable for drug developers.
    """
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text
```

---

## PHASE 5: Deployment & Testing (Day 2 - Evening)

### Step 5.1: Deploy Frontend
Options:
- **Vercel** (recommended, 1-click deploy from GitHub)
- **Netlify** (similar, free tier)
- **Antigravity hosting** (built-in)

### Step 5.2: Test the Complete Flow
1. Enter test SMILES: `CC(=O)OC1=CC=CC=C1C(=O)O` (aspirin)
2. Verify prediction returns within 2 seconds
3. Check database stores the result
4. Verify dashboard updates
5. Test edge cases (invalid SMILES, ambiguous molecules)

### Step 5.3: Add Error Handling
```javascript
// Frontend error handling
try {
  const response = await axios.post('/predict', { smiles });
} catch (error) {
  if (error.response.status === 400) {
    alert('Invalid SMILES format');
  } else if (error.response.status === 500) {
    alert('ML pipeline error. Try again.');
  }
}
```

---

## PHASE 6: Hackathon Submission Prep (Day 2 - Late Evening)

### Step 6.1: Documentation
Create `README.md` with:
- Architecture diagram
- Setup instructions
- API documentation
- Example predictions
- Model performance metrics

### Step 6.2: Demo Script
Prepare 5 test cases:
1. **High toxicity example**: Benzene derivative
2. **Low toxicity example**: Ethanol-like compound
3. **Borderline case**: Ambiguous molecule
4. **Drug example**: Aspirin or Ibuprofen
5. **Edge case**: Very large molecule

### Step 6.3: Create Presentation
Show judges:
1. **Problem**: Why toxicity prediction matters
2. **Solution**: Your architecture + Claude/Antigravity integration
3. **Model Performance**: Accuracy, F1 score (target 85%+)
4. **Live Demo**: Real prediction on stage
5. **Biological Insights**: What the model learned about drug toxicity
6. **Impact**: How many failed compounds could be caught early

---

## Key Success Metrics for Judges

| Metric | Target | Why It Matters |
|--------|--------|----------------|
| Model Accuracy | 85%+ | Shows ML competence |
| Feature Interpretability | Top 5 factors explained | Judges love SHAP/interpretability |
| API Response Time | <2 seconds | Performance matters |
| UI/UX Quality | Professional-looking | First impressions count |
| Biological Insights | 3-4 key findings | Domain understanding |
| Code Quality | Clean, documented | Hackathon best practices |

---

## Timeline Summary

| When | What | Deliverable |
|------|------|-------------|
| Day 1 - 8am | Antigravity backend setup | Database + 3 API endpoints |
| Day 1 - 12pm | Claude ML code generation | Python pipeline + model.pkl |
| Day 1 - 6pm | Frontend development | React prediction interface |
| Day 1 - 11pm | Integration testing | End-to-end flow working |
| Day 2 - 10am | Dashboard + visualizations | Feature importance charts |
| Day 2 - 2pm | Claude API interpretation | Biological explanations |
| Day 2 - 6pm | Testing + bug fixes | Polished, production-ready |
| Day 2 - 9pm | Documentation + slides | README + presentation |

---

## Pro Tips for Winning

✅ **Focus on insights, not code** - Judges care more about biological findings than perfect code

✅ **Use Claude for explanations** - Generate readable insights from raw predictions

✅ **Make the demo interactive** - Live predictions on stage are memorable

✅ **Document everything** - Well-documented code shows professionalism

✅ **Emphasize real-world impact** - "Could save $1M per failed compound" is compelling

✅ **Show feature importance** - SHAP values prove you understand what the model learned

---

## Questions to Prepare Answers For

1. **Why XGBoost over neural networks?** → Faster training, better interpretability, SHAP compatible
2. **How did you validate the model?** → 5-fold cross-validation, test set performance
3. **What's the false positive rate?** → Important for drug development
4. **Can the model handle unseen chemical scaffolds?** → Discuss generalization
5. **How would you deploy this in a real pharma company?** → Discuss scalability with Antigravity

