import pandas as pd
import numpy as np

def compute_time_features(df: pd.DataFrame, datetime_col: str = 'timestamp') -> pd.DataFrame:
    """Compute time-based features."""
    df = df.copy()
    
    if datetime_col in df.columns:
        dt = pd.to_datetime(df[datetime_col])
    else:
        dt = pd.to_datetime(df.index)
        
    hour = dt.dt.hour
    day = dt.dt.dayofweek
    
    df['hour_sin'] = np.sin(2 * np.pi * hour / 24)
    df['hour_cos'] = np.cos(2 * np.pi * hour / 24)
    df['day_sin'] = np.sin(2 * np.pi * day / 7)
    df['day_cos'] = np.cos(2 * np.pi * day / 7)
    
    # Session encoding: 0=Asian (0-8), 1=European (8-16), 2=American (16-24)
    df['session_type'] = pd.cut(hour, bins=[-1, 8, 16, 24], labels=[0, 1, 2], right=False).astype(float)
    df['is_weekend'] = (day >= 5).astype(int)
    
    return df
