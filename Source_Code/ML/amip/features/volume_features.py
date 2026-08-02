import pandas as pd
import numpy as np
import ta

def compute_volume_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute volume features."""
    df = df.copy()
    
    df['volume_change'] = df['volume'].pct_change()
    df['volume_sma20'] = df['volume'].rolling(window=20).mean()
    
    # Volume spike
    df['volume_spike'] = (df['volume'] > 2 * df['volume_sma20']).astype(int)
    
    # On-Balance Volume
    df['obv'] = ta.volume.on_balance_volume(df['close'], df['volume'])
    
    # VWAP Approximation (daily reset not required here, just simple rolling proxy)
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    df['vwap'] = (typical_price * df['volume']).cumsum() / df['volume'].cumsum()
    
    # Volume divergence: Price goes up, volume goes down
    df['price_up'] = df['close'] > df['close'].shift(1)
    df['vol_down'] = df['volume'] < df['volume'].shift(1)
    df['volume_divergence'] = (df['price_up'] & df['vol_down']).astype(int)
    
    df.drop(columns=['price_up', 'vol_down'], inplace=True)
    return df
