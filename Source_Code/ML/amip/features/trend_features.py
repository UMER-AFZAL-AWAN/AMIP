import pandas as pd
import numpy as np
import ta

def compute_trend_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute trend-based features."""
    df = df.copy()
    
    for period in [9, 21, 50, 200]:
        df[f'ema{period}'] = ta.trend.ema_indicator(df['close'], window=period)
        
    for period in [20, 50, 200]:
        df[f'sma{period}'] = ta.trend.sma_indicator(df['close'], window=period)
        
    # Trend direction based on EMA alignment
    # 1: strong uptrend (9 > 21 > 50), -1: strong downtrend (9 < 21 < 50), 0: mixed
    uptrend = (df['ema9'] > df['ema21']) & (df['ema21'] > df['ema50'])
    downtrend = (df['ema9'] < df['ema21']) & (df['ema21'] < df['ema50'])
    df['trend_direction'] = 0
    df.loc[uptrend, 'trend_direction'] = 1
    df.loc[downtrend, 'trend_direction'] = -1
    
    # Trend strength: average slope of EMAs
    df['trend_strength'] = df['ema21'].pct_change()
    
    # MA compression/expansion
    df['ma_compression'] = (df['ema9'] - df['ema50']) / df['ema50']
    
    return df
