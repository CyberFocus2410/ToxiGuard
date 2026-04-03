-- Predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255),
    smiles TEXT NOT NULL,
    toxicity_prob FLOAT NOT NULL,
    toxicity_category VARCHAR(20),
    risk_factors JSONB,
    confidence FLOAT,
    interpretation TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Model metadata
CREATE TABLE IF NOT EXISTS model_metadata (
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
CREATE TABLE IF NOT EXISTS feature_importance (
    id SERIAL PRIMARY KEY,
    model_version VARCHAR(50),
    feature_name VARCHAR(100),
    importance_score FLOAT,
    rank INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_predictions_user ON predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_predictions_created ON predictions(created_at);
CREATE INDEX IF NOT EXISTS idx_feature_version ON feature_importance(model_version);
