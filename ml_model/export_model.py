import os
import pandas as pd
from ml_pipeline import ToxicityPredictor

def build_production_model():
    """
    Builds and saves the initial toxicity model using the sample dataset.
    This ensures the web app has a 'toxicity_model.pkl' to load on startup.
    """
    print("=== CodeCure Model Builder ===")
    
    # Paths
    data_path = os.path.join(os.path.dirname(__file__), "tox21_full.csv")
    model_dir = os.path.join(os.path.dirname(__file__), "models")
    model_path = os.path.join(model_dir, "toxicity_model.pkl")
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print(f"Created directory: {model_dir}")
        
    # Initialize and train
    predictor = ToxicityPredictor()
    success = predictor.train(data_path)
    
    if success:
        print(f"Saving model to {model_path}...")
        predictor.save_model(model_path)
        print("Model export successful!")
    else:
        print("Model training failed. Check dependencies (rdkit, xgboost, shap).")

if __name__ == "__main__":
    build_production_model()
