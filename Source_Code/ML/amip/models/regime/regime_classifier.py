import pandas as pd
import numpy as np
from typing import Dict, Union, List
import xgboost as xgb
from skl2onnx.common.data_types import FloatTensorType
from onnxmltools.convert import convert_xgboost
from ..base_model import BaseModel

class RegimeClassifier(BaseModel):
    """Classify market into regimes based on features."""
    
    REGIMES = [
        "StrongUptrend", "WeakUptrend", "StrongDowntrend", "WeakDowntrend",
        "Sideways", "HighVolatility", "LowVolatility", "Accumulation", "Distribution"
    ]
    
    def __init__(self, model_name: str = "regime_classifier", **kwargs):
        super().__init__(model_name, **kwargs)
        self.model = xgb.XGBClassifier(objective='multi:softprob', num_class=len(self.REGIMES), **self.params)
        
    def generate_labels(self, df: pd.DataFrame) -> pd.Series:
        """Heuristic-based labeling for training regime classifier."""
        labels = pd.Series(np.zeros(len(df)), index=df.index, dtype=int)
        
        # We assume df has trend_direction, volatility_regime, ma_compression etc.
        # Strong Uptrend
        su = (df.get('trend_direction', 0) == 1) & (df.get('trend_strength', 0) > 0.01)
        labels[su] = 0
        
        # Weak Uptrend
        wu = (df.get('trend_direction', 0) == 1) & (df.get('trend_strength', 0) <= 0.01)
        labels[wu] = 1
        
        # Strong Downtrend
        sd = (df.get('trend_direction', 0) == -1) & (df.get('trend_strength', 0) < -0.01)
        labels[sd] = 2
        
        # Weak Downtrend
        wd = (df.get('trend_direction', 0) == -1) & (df.get('trend_strength', 0) >= -0.01)
        labels[wd] = 3
        
        # High Volatility
        hv = df.get('volatility_regime', 0) == 1
        # Overwrite if highly volatile
        labels[hv] = 5
        
        # Sideways / Low Vol
        lv = (df.get('volatility_regime', 0) == 0) & (df.get('trend_direction', 0) == 0)
        labels[lv] = 4
        
        return labels

    def train(self, X_train: pd.DataFrame, y_train: Union[pd.Series, np.ndarray] = None,
              X_val: pd.DataFrame = None, y_val: Union[pd.Series, np.ndarray] = None) -> Dict[str, float]:
        
        if y_train is None:
            y_train = self.generate_labels(X_train)
            
        eval_set = [(X_train, y_train)]
        if X_val is not None:
            if y_val is None:
                y_val = self.generate_labels(X_val)
            eval_set.append((X_val, y_val))
            
        self.model.fit(X_train, y_train, eval_set=eval_set, verbose=False)
        metrics = self.evaluate(X_train, y_train)
        if X_val is not None:
            val_metrics = self.evaluate(X_val, y_val)
            metrics.update({f"val_{k}": v for k, v in val_metrics.items()})
        return metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)
        
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict_proba(X)
        
    def get_regime_name(self, idx: int) -> str:
        return self.REGIMES[idx] if 0 <= idx < len(self.REGIMES) else "Unknown"
        
    def export_onnx(self, filepath: str, input_shape: tuple) -> None:
        initial_type = [('float_input', FloatTensorType([None, input_shape[1]]))]
        onx = convert_xgboost(self.model, initial_types=initial_type)
        with open(filepath, "wb") as f:
            f.write(onx.SerializeToString())
