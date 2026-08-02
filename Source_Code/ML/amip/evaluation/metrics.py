import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from typing import Dict, Union

def calculate_classification_metrics(y_true: Union[pd.Series, np.ndarray], y_pred: Union[pd.Series, np.ndarray]) -> Dict[str, float]:
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'f1': f1_score(y_true, y_pred, average='weighted', zero_division=0)
    }

def calculate_financial_metrics(returns: Union[pd.Series, np.ndarray], risk_free_rate: float = 0.0) -> Dict[str, float]:
    """Calculate financial metrics like Sharpe, Sortino, max drawdown."""
    ret = pd.Series(returns) if not isinstance(returns, pd.Series) else returns
    if len(ret) == 0:
        return {}
        
    cum_returns = (1 + ret).cumprod()
    total_return = cum_returns.iloc[-1] - 1 if len(cum_returns) > 0 else 0
    
    annualized_return = total_return * (252 / len(ret)) if len(ret) > 0 else 0
    annualized_volatility = ret.std() * np.sqrt(252) if len(ret) > 1 else 0
    
    sharpe = (annualized_return - risk_free_rate) / annualized_volatility if annualized_volatility > 0 else 0
    
    downside_ret = ret[ret < 0]
    downside_vol = downside_ret.std() * np.sqrt(252) if len(downside_ret) > 1 else 0
    sortino = (annualized_return - risk_free_rate) / downside_vol if downside_vol > 0 else 0
    
    running_max = cum_returns.cummax()
    drawdown = (cum_returns - running_max) / running_max
    max_drawdown = drawdown.min() if len(drawdown) > 0 else 0
    
    wins = ret[ret > 0].sum()
    losses = abs(ret[ret < 0].sum())
    profit_factor = wins / losses if losses > 0 else float('inf')
    win_rate = len(ret[ret > 0]) / len(ret) if len(ret) > 0 else 0
    
    return {
        'total_return': float(total_return),
        'annualized_return': float(annualized_return),
        'sharpe_ratio': float(sharpe),
        'sortino_ratio': float(sortino),
        'max_drawdown': float(max_drawdown),
        'profit_factor': float(profit_factor),
        'win_rate': float(win_rate)
    }
