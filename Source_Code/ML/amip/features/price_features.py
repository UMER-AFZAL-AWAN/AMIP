import pandas as pd
import numpy as np

def compute_price_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute price-based features."""
    df = df.copy()
    
    df['log_return'] = np.log(df['close'] / df['close'].shift(1))
    df['pct_change'] = df['close'].pct_change()
    df['price_momentum'] = df['close'] - df['close'].shift(5)
    
    # Candle structure
    df['range'] = df['high'] - df['low']
    # Avoid division by zero
    range_safe = df['range'].replace(0, 1e-8)
    
    df['candle_body_ratio'] = np.abs(df['close'] - df['open']) / range_safe
    df['upper_wick_ratio'] = (df['high'] - df[['open', 'close']].max(axis=1)) / range_safe
    df['lower_wick_ratio'] = (df[['open', 'close']].min(axis=1) - df['low']) / range_safe
    
    df['bullish_strength'] = (df['close'] - df['low']) / range_safe
    df['price_acceleration'] = df['log_return'] - df['log_return'].shift(1)
    
    # Distance from MA
    df['sma20'] = df['close'].rolling(window=20).mean()
    df['distance_from_ma'] = (df['close'] - df['sma20']) / df['sma20']
    df.drop(columns=['range', 'sma20'], inplace=True)
    
    return df
