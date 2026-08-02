import pandas as pd
import numpy as np
import ta

def compute_volatility_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute volatility features."""
    df = df.copy()
    
    df['atr14'] = ta.volatility.average_true_range(df['high'], df['low'], df['close'], window=14)
    
    df['daily_return'] = df['close'].pct_change()
    df['historical_volatility20'] = df['daily_return'].rolling(window=20).std() * np.sqrt(252)
    df['rolling_std20'] = df['close'].rolling(window=20).std()
    
    bb = ta.volatility.BollingerBands(df['close'], window=20, window_dev=2)
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()
    df['bb_mid'] = bb.bollinger_mavg()
    df['bb_width'] = bb.bollinger_wband()
    df['bb_pct'] = bb.bollinger_pband()
    
    # Volatility regime: High if hist vol is above its 200-day average
    mean_vol = df['historical_volatility20'].rolling(window=200).mean()
    df['volatility_regime'] = (df['historical_volatility20'] > mean_vol).astype(int)
    
    df.drop(columns=['daily_return'], inplace=True)
    return df
