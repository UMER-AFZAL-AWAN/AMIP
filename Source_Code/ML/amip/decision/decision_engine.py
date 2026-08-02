from typing import Dict, Any, List

class DecisionEngine:
    """Combines inputs from multiple models to make a final trading decision."""
    
    def __init__(self, risk_tolerance: float = 0.5):
        self.risk_tolerance = risk_tolerance
        
    def evaluate(self, 
                 regime_probs: List[float], 
                 regime_name: str,
                 pattern_similarity: float, 
                 prediction_prob: float, 
                 volatility: float) -> Dict[str, Any]:
        """
        Combine all signals into a final decision.
        """
        confidence = 0.0
        decision = "HOLD"
        risk_level = "LOW"
        
        if volatility > 0.02:
            risk_level = "HIGH"
        elif volatility > 0.01:
            risk_level = "MEDIUM"
            
        # Base signal from prediction
        if prediction_prob > 0.65:
            decision = "LONG"
            confidence = prediction_prob
        elif prediction_prob < 0.35:
            decision = "SHORT"
            confidence = 1 - prediction_prob
            
        # Adjust based on regime
        if regime_name == "StrongUptrend" and decision == "LONG":
            confidence += 0.1
        elif regime_name == "StrongDowntrend" and decision == "SHORT":
            confidence += 0.1
        elif regime_name in ["HighVolatility", "Sideways"] and risk_level == "HIGH":
            # Override if risk is too high
            decision = "HOLD"
            confidence = 0.0
            
        # Adjust based on pattern similarity
        if pattern_similarity > 0.8:
            confidence += 0.15
            
        # Cap confidence
        confidence = min(1.0, confidence)
        
        # Final risk check
        if risk_level == "HIGH" and confidence < (0.7 + (1-self.risk_tolerance)):
            decision = "HOLD"
            
        return {
            'decision': decision,
            'confidence': confidence,
            'risk_level': risk_level,
            'expected_scenarios': [
                "Continuation of current trend" if confidence > 0.7 else "Possible reversal or consolidation",
                f"Regime: {regime_name}"
            ]
        }
