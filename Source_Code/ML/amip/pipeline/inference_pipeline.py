import pandas as pd
import numpy as np
from typing import Dict, Any
from ..features.feature_pipeline import FeaturePipeline

class InferencePipeline:
    def __init__(self, model):
        self.model = model
        self.feature_pipeline = FeaturePipeline()
        
    def predict(self, raw_data: pd.DataFrame) -> Dict[str, Any]:
        """Real-time inference pipeline."""
        # Feature Engineering
        features = self.feature_pipeline.transform(raw_data)
        
        if len(features) == 0:
            return {"error": "Not enough data to compute features"}
            
        # Extract last row for prediction
        last_row = features.iloc[[-1]]
        X = last_row.drop(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'target'], errors='ignore')
        
        # Inference
        probs = self.model.predict_proba(X)
        pred = self.model.predict(X)
        
        return {
            'prediction': int(pred[0]),
            'probabilities': probs[0].tolist(),
            'features_used': X.to_dict('records')[0]
        }
