import os
import json
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    print("Warning: google-generativeai package not installed. AI interpretation will be simulation-based.")

class AIInterpretationService:
    def __init__(self):
        # API key should be set in environment as GOOGLE_API_KEY
        self.api_key = os.getenv('GOOGLE_API_KEY', '')
        self.model = None
        
        if self.api_key and HAS_GEMINI:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-1.5-pro')
            except Exception as e:
                print(f"Error initializing Gemini AI: {e}")

    def generate_interpretation(self, prediction_data):
        """
        Calls Gemini AI to interpret the toxicity prediction result.
        
        Args:
            prediction_data (dict): Data from the ML pipeline including toxicity_prob, 
                                     category, and risk_factors.
        Returns:
            str: Human-readable biological interpretation.
        """
        smiles = prediction_data.get('smiles', 'Unknown Organic Molecule')
        prob = prediction_data.get('toxicity_probability', 0.0)
        category = prediction_data.get('toxicity_category', 'Low')
        factors = prediction_data.get('risk_factors', [])
        
        factor_strings = [f"{f['feature']} ({f['contribution']})" for f in factors[:3]]
        
        prompt = f"""
        System: You are a world-class pharmaceutical toxicology expert. Be concise and scientifically precise.
        
        User: A ToxiGuard ML model analyzed compound: {smiles}
        Predicted toxicity: {prob*100:.1f}% | Risk: {category}
        Top risk factors: {', '.join(factor_strings)}
        
        Provide a professional biological interpretation in under 150 words:
        1) Analyze the structural toxicity profile.
        2) Identify specific molecular properties contributing to the risk.
        3) Suggest structural modifications to improve safety while maintaining efficacy.
        """
        
        if self.model:
            try:
                response = self.model.generate_content(prompt)
                return response.text
            except Exception as e:
                print(f"Gemini API error: {e}")
                return self._mock_interpretation(category, factors)
        else:
            return self._mock_interpretation(category, factors)

    def _mock_interpretation(self, category, factors):
        """Fallback mock interpretation for local testing or missing API key"""
        if category == 'High':
            return (f"[SIMULATION] Analysis indicates high toxicity potential driven by {factors[0]['feature'] if factors else 'aromaticity'}. "
                    "The structure may induce oxidative stress or have electrophilic segments. Consider reducing lipophilicity to improve safety.")
        elif category == 'Medium':
            return (f"[SIMULATION] Moderate toxicity risk observed. Descriptor {factors[0]['feature'] if factors else 'Toxophore'} "
                    "suggests a potential for non-specific binding. Optimization of scaffold flexibility is recommended.")
        else:
            return (f"[SIMULATION] Compound shows a favorable safety profile. {factors[0]['feature'] if factors else 'Parameters'} "
                    "align with safe drug-like molecular space. Recommended for continued development.")

# Singleton instance
ai_service = AIInterpretationService()
