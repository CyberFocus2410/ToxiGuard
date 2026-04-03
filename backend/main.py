import json
from ml_model.ml_pipeline import ToxicityPredictor
from ai_service import ai_service

# Initialize predictor
predictor = ToxicityPredictor("models/toxicity_model.pkl")

def handle_prediction_request(smiles, user_id=None):
    """
    Main entry point for handling toxicity prediction requests.
    Ties together the ML pipeline and AI interpretation service.
    
    Args:
        smiles (str): SMILES representation of the molecule.
        user_id (str): Optional identifier of the requesting user.
    Returns:
        dict: Complete prediction response for the API.
    """
    try:
        # Step 1: Run ML Prediction
        print(f"Analyzing MOLECULE: {smiles} for user {user_id or 'Demo'}")
        
        # Step 1.1: SMILES Validation
        if not smiles or not isinstance(smiles, str) or len(smiles) < 1:
            return {"error": "Invalid SMILES format", "code": 400}
            
        # Step 2: Prediction
        result = predictor.predict(smiles)
        result['smiles'] = smiles
        
        # Step 3: AI Interpretation
        print("Requesting AI interpretation from Claude...")
        interpretation = ai_service.generate_interpretation(result)
        result['interpretation'] = interpretation
        
        # Step 4: Finalize response
        # In a real Antigravity workflow, this would also include a DB write step
        # like: db.insert('predictions', **result)
        
        return result
    except Exception as e:
        print(f"Error in prediction workflow: {e}")
        return {"error": "System encountered an error. Check logs.", "code": 500}

# Testing the workflow
if __name__ == "__main__":
    test_smiles = "CCO" # Ethanol
    response = handle_prediction_request(test_smiles)
    print("\n[PREDICTION RESPONSE]")
    print(json.dumps(response, indent=2))
