import pandas as pd
import numpy as np
from typing import Dict, Union
from sklearn.ensemble import RandomForestClassifier
from skl2onnx import convert_sklearn
from skl2onnx.common.data_types import FloatTensorType
from ..base_model import BaseModel

class RandomForestModel(BaseModel):
    def __init__(self, model_name: str = "random_forest", **kwargs):
        super().__init__(model_name, **kwargs)
        self.model = RandomForestClassifier(**self.params)
        
    def train(self, X_train: pd.DataFrame, y_train: Union[pd.Series, np.ndarray],
              X_val: pd.DataFrame = None, y_val: Union[pd.Series, np.ndarray] = None) -> Dict[str, float]:
        self.model.fit(X_train, y_train)
        metrics = self.evaluate(X_train, y_train)
        if X_val is not None and y_val is not None:
            val_metrics = self.evaluate(X_val, y_val)
            metrics.update({f"val_{k}": v for k, v in val_metrics.items()})
        return metrics

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)
        
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict_proba(X)
        
    def export_onnx(self, filepath: str, input_shape: tuple) -> None:
        initial_type = [('float_input', FloatTensorType([None, input_shape[1]]))]
        onx = convert_sklearn(self.model, initial_types=initial_type)
        with open(filepath, "wb") as f:
            f.write(onx.SerializeToString())
