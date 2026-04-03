import os
import json
try:
    import anthropic
except ImportError:
    print("Warning: anthropic package not installed. AI interpretation will be simulation-based.")

class AIInterpretationService:
    def __init__(self):
        # API key should be set in environment as ANTHROPIC_API_KEY
        self.api_key = os.getenv('ANTHROPIC_API_KEY', 'MOCK_KEY')
        self.client = None
        
        if self.api_key != 'MOCK_KEY':
            try:
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except Exception as e:
                print(f"Error initializing AI client: {e}")

    def generate_interpretation(self, prediction_data):
        """
        Calls Claude API to interpret the toxicity prediction result.
        
        Args:
            prediction_data (dict): Data from the ML pipeline including toxicity_prob, 
                                     category, and risk_factors.
        Returns:
            str: Human-readable biological interpretation.
        """
        smiles = prediction_data.get('smiles', 'Unknown')
        prob = prediction_data.get('toxicity_probability', 0.0)
        category = prediction_data.get('toxicity_category', 'Low')
        factors = prediction_data.get('risk_factors', [])
        
        factor_strings = [f"{f['feature']} ({f['contribution']})" for f in factors[:3]]
        
        prompt = f"""
        System: You are a pharmaceutical toxicology expert. Be concise and scientifically precise.
        
        User: A drug toxicity prediction model analyzed compound: {smiles}
        Predicted toxicity: {prob*100:.1f}% | Risk: {category}
        Top risk factors: {', '.join(factor_strings)}
        
        Explain in under 150 words:
        1) Why this compound might show {category} toxicity risk.
        2) Which specific molecular properties (risk factors) contribute most.
        3) What structural modifications could potentially reduce this toxicity.
        """
        
        if self.client:
            try:
                message = self.client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                return message.content[0].text
            except Exception as e:
                print(f"AI Interpretation API error: {e}")
                return self._mock_interpretation(category, factors)
        else:
            return self._mock_interpretation(category, factors)

    def _mock_interpretation(self, category, factors):
        """Fallback mock interpretation for local testing or missing API key"""
        if category == 'High':
            return (f"The analysis indicates high toxicity potential, primarily driven by {factors[0]['feature'] if factors else 'molecular complexity'}. "
                    "The compound likely interacts with essential cellular pathways or induces oxidative stress. "
                    "Reducing lipophilicity or removing aromatic halogen groups might improve the safety profile.")
        elif category == 'Medium':
            return (f"Moderate toxicity risk is observed. The contribution of {factors[0]['feature'] if factors else 'polar surface area'} "
                    "suggests potential for off-target binding. Consider optimizing the scaffold flexibility to reduce binding affinity to common toxicological targets.")
        else:
            return (f"The compound has a favorable toxicological profile. The {factors[0]['feature'] if factors else 'descriptors'} "
                    "align with known safe drug-like spaces. Maintaining the current structure is recommended for continued development.")

# Singleton instance
ai_service = AIInterpretationService()
