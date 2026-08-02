import pandas as pd
from typing import Dict, Any
from ..features.feature_pipeline import FeaturePipeline
from ..models.baseline.xgboost_model import XGBoostModel
from ..models.regime.regime_classifier import RegimeClassifier
from ..utils.experiment_tracker import ExperimentTracker

class TrainingPipeline:
    def __init__(self):
        self.feature_pipeline = FeaturePipeline()
        self.tracker = ExperimentTracker()
        
    def run(self, raw_data: pd.DataFrame, target_col: str = 'target', model_type: str = 'xgboost') -> Dict[str, Any]:
        """End-to-end training pipeline."""
        # 1. Feature Engineering
        features = self.feature_pipeline.transform(raw_data)
        
        if target_col not in features.columns:
            # Generate dummy target for testing: 1 if next close > close
            features[target_col] = (features['close'].shift(-1) > features['close']).astype(int)
            features.dropna(inplace=True)
            
        X = features.drop(columns=[target_col, 'timestamp', 'open', 'high', 'low', 'close', 'volume'], errors='ignore')
        y = features[target_col]
        
        # Split
        split_idx = int(len(X) * 0.8)
        X_train, X_val = X.iloc[:split_idx], X.iloc[split_idx:]
        y_train, y_val = y.iloc[:split_idx], y.iloc[split_idx:]
        
        # 2. Train Model
        if model_type == 'xgboost':
            model = XGBoostModel()
        elif model_type == 'regime':
            model = RegimeClassifier()
        else:
            raise ValueError(f"Unknown model type: {model_type}")
            
        metrics = model.train(X_train, y_train, X_val, y_val)
        
        # 3. Log experiment
        exp_id = self.tracker.log_experiment(
            model_name=model_type,
            parameters=model.params,
            metrics=metrics
        )
        
        return {
            'experiment_id': exp_id,
            'metrics': metrics,
            'model': model,
            'features': list(X.columns)
        }
