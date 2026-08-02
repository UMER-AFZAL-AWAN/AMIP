import pandas as pd
from typing import Optional
from .price_features import compute_price_features
from .trend_features import compute_trend_features
from .momentum_features import compute_momentum_features
from .volatility_features import compute_volatility_features
from .volume_features import compute_volume_features
from .market_structure import compute_market_structure
from .time_features import compute_time_features

class FeaturePipeline:
    """Orchestrates all feature computation."""
    
    def __init__(self, use_time_features: bool = True):
        self.use_time_features = use_time_features
        
    def transform(self, df: pd.DataFrame, datetime_col: Optional[str] = 'timestamp') -> pd.DataFrame:
        """
        Apply all feature engineering steps to the input dataframe.
        Expects columns: open, high, low, close, volume.
        """
        result = df.copy()
        
        result = compute_price_features(result)
        result = compute_trend_features(result)
        result = compute_momentum_features(result)
        result = compute_volatility_features(result)
        result = compute_volume_features(result)
        result = compute_market_structure(result)
        
        if self.use_time_features:
            result = compute_time_features(result, datetime_col=datetime_col)
            
        return result.dropna()
