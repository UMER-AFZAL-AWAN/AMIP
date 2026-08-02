import pandas as pd
import numpy as np
from typing import Dict, Union
import lightgbm as lgb
from skl2onnx.common.data_types import FloatTensorType
from onnxmltools.convert import convert_lightgbm
from ..base_model import BaseModel

class LightGBMModel(BaseModel):
    def __init__(self, model_name: str = "lightgbm", **kwargs):
        super().__init__(model_name, **kwargs)
        self.model = lgb.LGBMClassifier(**self.params)
        
    def train(self, X_train: pd.DataFrame, y_train: Union[pd.Series, np.ndarray],
              X_val: pd.DataFrame = None, y_val: Union[pd.Series, np.ndarray] = None) -> Dict[str, float]:
        eval_set = [(X_train, y_train)]
        if X_val is not None and y_val is not None:
            eval_set.append((X_val, y_val))
            
        self.model.fit(X_train, y_train, eval_set=eval_set)
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
        onx = convert_lightgbm(self.model, initial_types=initial_type)
        with open(filepath, "wb") as f:
            f.write(onx.SerializeToString())
