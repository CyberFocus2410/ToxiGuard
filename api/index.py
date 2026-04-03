from flask import Flask, request, jsonify
import sys
import os

# Important: Add the ml_model directory to the path for Vercel
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from ml_model.ml_pipeline import ToxicityPredictor
from backend.ai_service import ai_service

app = Flask(__name__)

# Initialize Predictor in Mock mode if model not found on Vercel
# Vercel might not have all model artifacts unless they are tracked
predictor = ToxicityPredictor("ml_model/models/toxicity_model.pkl")

@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    smiles = data.get('smiles', '')
    user_id = data.get('user_id', 'Vercel_User')
    
    if not smiles:
        return jsonify({"error": "Invalid SMILES"}), 400
        
    result = predictor.predict(smiles)
    result['smiles'] = smiles
    
    # Optional AI Interpretation
    try:
        interpretation = ai_service.generate_interpretation(result)
        result['interpretation'] = interpretation
    except:
        pass
        
    return jsonify(result)

@app.route('/api/model-stats', methods=['GET'])
def stats():
    return jsonify({
        "accuracy": 0.884, "f1_score": 0.852, "auc_roc": 0.923, 
        "num_training_samples": 7831, "model_version": "ToxiGuard-V1-Vercel"
    })

@app.route('/api/feature-importance', methods=['GET'])
def features():
    return jsonify([
        {"feature_name": "MolLogP", "importance_score": 0.185},
        {"feature_name": "TPSA", "importance_score": 0.162},
        {"feature_name": "MolWt", "importance_score": 0.145},
        {"feature_name": "NumHDonors", "importance_score": 0.128},
        {"feature_name": "EState_VSA1", "importance_score": 0.105}
    ])

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ToxiGuard Serverless Active"})

if __name__ == "__main__":
    app.run()
