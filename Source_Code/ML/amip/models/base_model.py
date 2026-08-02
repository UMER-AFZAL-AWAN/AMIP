import abc
import os
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, Union

class BaseModel(abc.ABC):
    """Abstract base class for all models."""
    
    def __init__(self, model_name: str, **kwargs):
        self.model_name = model_name
        self.params = kwargs
        self.model = None
        
    @abc.abstractmethod
    def train(self, X_train: pd.DataFrame, y_train: Union[pd.Series, np.ndarray], 
              X_val: pd.DataFrame = None, y_val: Union[pd.Series, np.ndarray] = None) -> Dict[str, float]:
        """Train the model and return metrics."""
        pass
        
    @abc.abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predict class labels or values."""
        pass
        
    @abc.abstractmethod
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """Predict probabilities."""
        pass
        
    def evaluate(self, X: pd.DataFrame, y: Union[pd.Series, np.ndarray]) -> Dict[str, float]:
        """Evaluate model performance."""
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
        preds = self.predict(X)
        return {
            'accuracy': accuracy_score(y, preds),
            'precision': precision_score(y, preds, average='weighted', zero_division=0),
            'recall': recall_score(y, preds, average='weighted', zero_division=0),
            'f1': f1_score(y, preds, average='weighted', zero_division=0)
        }
        
    def save(self, filepath: str) -> None:
        """Save model to disk."""
        if self.model is None:
            raise ValueError("Model is not trained.")
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        
    def load(self, filepath: str) -> None:
        """Load model from disk."""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        self.model = joblib.load(filepath)
        
    @abc.abstractmethod
    def export_onnx(self, filepath: str, input_shape: tuple) -> None:
        """Export model to ONNX format."""
        pass
