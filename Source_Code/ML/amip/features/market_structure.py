import pandas as pd
import numpy as np

def compute_market_structure(df: pd.DataFrame) -> pd.DataFrame:
    """Compute market structure features like HH/HL/LH/LL."""
    df = df.copy()
    
    window = 5
    
    # Local max and min
    df['local_max'] = df['high'] == df['high'].rolling(window=window*2+1, center=True).max()
    df['local_min'] = df['low'] == df['low'].rolling(window=window*2+1, center=True).min()
    
    df['last_swing_high'] = df['high'].where(df['local_max']).ffill()
    df['last_swing_low'] = df['low'].where(df['local_min']).ffill()
    
    prev_high = df['last_swing_high'].shift(1)
    prev_low = df['last_swing_low'].shift(1)
    
    df['higher_high'] = (df['local_max'] & (df['high'] > prev_high)).astype(int)
    df['lower_high'] = (df['local_max'] & (df['high'] < prev_high)).astype(int)
    df['higher_low'] = (df['local_min'] & (df['low'] > prev_low)).astype(int)
    df['lower_low'] = (df['local_min'] & (df['low'] < prev_low)).astype(int)
    
    # Distance to support/resistance
    df['dist_to_res'] = (df['last_swing_high'] - df['close']) / df['close']
    df['dist_to_sup'] = (df['close'] - df['last_swing_low']) / df['close']
    
    df.drop(columns=['local_max', 'local_min'], inplace=True)
    
    return df
