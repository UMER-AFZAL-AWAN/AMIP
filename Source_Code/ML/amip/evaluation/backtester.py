import pandas as pd
import numpy as np
from typing import Dict, List, Any
from .metrics import calculate_classification_metrics, calculate_financial_metrics

class WalkForwardBacktester:
    """Walk-forward backtesting engine to prevent look-ahead bias."""
    
    def __init__(self, model, train_window: int = 1000, test_window: int = 200):
        self.model = model
        self.train_window = train_window
        self.test_window = test_window
        
    def run(self, X: pd.DataFrame, y: pd.Series, returns: pd.Series) -> Dict[str, Any]:
        """
        Run walk forward backtest.
        X: Feature dataframe
        y: Target labels (for training/classification)
        returns: Next period returns (for financial metrics)
        """
        n_samples = len(X)
        if n_samples < self.train_window + self.test_window:
            raise ValueError("Not enough data for backtesting.")
            
        all_preds = []
        all_actuals = []
        all_returns = []
        
        for start_idx in range(0, n_samples - self.train_window, self.test_window):
            train_end = start_idx + self.train_window
            test_end = min(train_end + self.test_window, n_samples)
            
            X_train = X.iloc[start_idx:train_end]
            y_train = y.iloc[start_idx:train_end]
            
            X_test = X.iloc[train_end:test_end]
            y_test = y.iloc[train_end:test_end]
            ret_test = returns.iloc[train_end:test_end]
            
            self.model.train(X_train, y_train)
            preds = self.model.predict(X_test)
            
            # For simplicity, assuming pred=1 means long, pred=0 means short
            # Real logic might be more complex
            strategy_returns = np.where(preds == 1, ret_test, -ret_test)
            
            all_preds.extend(preds)
            all_actuals.extend(y_test)
            all_returns.extend(strategy_returns)
            
        cls_metrics = calculate_classification_metrics(all_actuals, all_preds)
        fin_metrics = calculate_financial_metrics(pd.Series(all_returns))
        
        baseline_returns = returns.iloc[self.train_window:len(X)]
        baseline_fin = calculate_financial_metrics(baseline_returns)
        
        return {
            'classification_metrics': cls_metrics,
            'strategy_metrics': fin_metrics,
            'baseline_metrics': baseline_fin,
            'predictions': all_preds,
            'actuals': all_actuals,
            'strategy_returns': all_returns
        }
