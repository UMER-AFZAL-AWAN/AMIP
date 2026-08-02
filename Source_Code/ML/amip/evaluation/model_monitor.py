import pandas as pd
import numpy as np
from scipy.stats import ks_2samp

class ModelMonitor:
    """Monitor models for data drift and performance degradation."""
    
    def __init__(self, reference_data: pd.DataFrame = None):
        self.reference_data = reference_data
        
    def set_reference(self, data: pd.DataFrame):
        self.reference_data = data
        
    def detect_drift(self, current_data: pd.DataFrame, alpha: float = 0.05) -> dict:
        """Detect drift using Kolmogorov-Smirnov test for numerical features."""
        if self.reference_data is None:
            raise ValueError("Reference data not set.")
            
        drift_results = {}
        for col in current_data.columns:
            if col in self.reference_data.columns and pd.api.types.is_numeric_dtype(current_data[col]):
                ref_vals = self.reference_data[col].dropna()
                cur_vals = current_data[col].dropna()
                
                if len(ref_vals) == 0 or len(cur_vals) == 0:
                    continue
                    
                stat, p_value = ks_2samp(ref_vals, cur_vals)
                is_drifting = p_value < alpha
                drift_results[col] = {
                    'statistic': stat,
                    'p_value': p_value,
                    'is_drifting': is_drifting
                }
                
        num_drifting = sum([1 for k, v in drift_results.items() if v['is_drifting']])
        return {
            'features': drift_results,
            'drifting_features_count': num_drifting,
            'total_features': len(drift_results),
            'dataset_drift': (num_drifting / len(drift_results)) > 0.2 if len(drift_results) > 0 else False
        }
