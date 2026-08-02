import pandas as pd
import numpy as np
import ta

def compute_momentum_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute momentum features."""
    df = df.copy()
    
    df['rsi14'] = ta.momentum.rsi(df['close'], window=14)
    
    macd = ta.trend.MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['macd_diff'] = macd.macd_diff()
    
    stoch = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'], window=14, smooth_window=3)
    df['stoch_k'] = stoch.stoch()
    df['stoch_d'] = stoch.stoch_signal()
    
    df['roc10'] = ta.momentum.roc(df['close'], window=10)
    
    # Momentum divergence
    # Simple check: price makes lower low, but RSI makes higher low
    df['price_ll'] = (df['low'] < df['low'].shift(1)) & (df['low'].shift(1) < df['low'].shift(2))
    df['rsi_hl'] = (df['rsi14'] > df['rsi14'].shift(1)) & (df['rsi14'].shift(1) > df['rsi14'].shift(2))
    df['bullish_divergence'] = (df['price_ll'] & df['rsi_hl']).astype(int)
    
    df['price_hh'] = (df['high'] > df['high'].shift(1)) & (df['high'].shift(1) > df['high'].shift(2))
    df['rsi_lh'] = (df['rsi14'] < df['rsi14'].shift(1)) & (df['rsi14'].shift(1) < df['rsi14'].shift(2))
    df['bearish_divergence'] = (df['price_hh'] & df['rsi_lh']).astype(int)
    
    df.drop(columns=['price_ll', 'rsi_hl', 'price_hh', 'rsi_lh'], inplace=True)
    return df
