"""
Train ML models from historical data stored in the PostgreSQL database.

Usage:
    python -m amip.pipeline.train_from_db --model xgboost --symbol BTCUSDT --days 30
    python -m amip.pipeline.train_from_db --model lightgbm --symbol BTCUSDT --days 60
    python -m amip.pipeline.train_from_db --model random_forest --symbol BTCUSDT --days 30
"""

import os
import sys
import argparse
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from amip.utils.database import get_engine, get_session, MarketCandle
from amip.features.feature_pipeline import FeaturePipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URI = "postgresql://amip_admin:amip_secure_2026@localhost:5432/amip_market_intelligence"
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Models/trained'))


def load_candles_from_db(symbol: str, days: int) -> pd.DataFrame:
    """Load historical candle data from PostgreSQL."""
    engine = get_engine(DB_URI)
    session = get_session(engine)

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    candles = session.query(MarketCandle)\
                     .filter(MarketCandle.Symbol == symbol)\
                     .filter(MarketCandle.CloseTime >= cutoff)\
                     .order_by(MarketCandle.CloseTime.asc())\
                     .all()

    session.close()

    if not candles:
        logger.error(f"No candles found for {symbol} in the last {days} days.")
        return pd.DataFrame()

    df = pd.DataFrame([{
        'timestamp': c.CloseTime,
        'open': c.Open,
        'high': c.High,
        'low': c.Low,
        'close': c.Close,
        'volume': c.Volume,
    } for c in candles])

    logger.info(f"Loaded {len(df)} candles for {symbol} from the database.")
    return df


def create_target(df: pd.DataFrame, horizon: int = 1) -> pd.DataFrame:
    """Create a binary target: 1 if close goes UP after `horizon` periods, else 0."""
    df = df.copy()
    df['target'] = (df['close'].shift(-horizon) > df['close']).astype(int)
    df.dropna(subset=['target'], inplace=True)
    df['target'] = df['target'].astype(int)
    return df


def get_model(model_type: str):
    """Instantiate a model by name."""
    if model_type == 'xgboost':
        from amip.models.baseline.xgboost_model import XGBoostModel
        return XGBoostModel(n_estimators=200, max_depth=5, learning_rate=0.05)
    elif model_type == 'lightgbm':
        from amip.models.baseline.lightgbm_model import LightGBMModel
        return LightGBMModel(n_estimators=200, max_depth=5, learning_rate=0.05)
    elif model_type == 'random_forest':
        from amip.models.baseline.random_forest import RandomForestModel
        return RandomForestModel(n_estimators=200, max_depth=10)
    elif model_type == 'logistic':
        from amip.models.baseline.logistic_model import LogisticModel
        return LogisticModel()
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def train(model_type: str, symbol: str, days: int):
    logger.info(f"=== Training {model_type} on {symbol} ({days} days) ===")

    # 1. Load data
    raw_df = load_candles_from_db(symbol, days)
    if raw_df.empty:
        return

    # 2. Feature engineering
    pipeline = FeaturePipeline()
    features_df = pipeline.transform(raw_df)
    logger.info(f"Computed {len(features_df.columns)} features on {len(features_df)} rows.")

    if len(features_df) < 100:
        logger.error("Not enough data to train. Need at least 100 rows after feature computation.")
        return

    # 3. Create target
    features_df = create_target(features_df, horizon=1)

    # 4. Prepare X and y
    drop_cols = ['target', 'timestamp', 'open', 'high', 'low', 'close', 'volume']
    X = features_df.drop(columns=[c for c in drop_cols if c in features_df.columns])
    y = features_df['target']

    # 5. Time-series split (80/20)
    split_idx = int(len(X) * 0.8)
    X_train, X_val = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_val = y.iloc[:split_idx], y.iloc[split_idx:]

    logger.info(f"Train: {len(X_train)} samples | Validation: {len(X_val)} samples")

    # 6. Train
    model = get_model(model_type)
    metrics = model.train(X_train, y_train, X_val, y_val)

    logger.info(f"Training metrics: {metrics}")

    # 7. Save model
    os.makedirs(MODELS_DIR, exist_ok=True)
    model_path = os.path.join(MODELS_DIR, f"{model_type}_{symbol}.joblib")
    model.save(model_path)
    logger.info(f"Model saved to {model_path}")

    # 8. Summary
    val_acc = metrics.get('val_accuracy', metrics.get('accuracy', 0))
    logger.info(f"=== Done! Validation Accuracy: {val_acc:.4f} ===")

    return metrics


def main():
    parser = argparse.ArgumentParser(description="Train ML models from database candle data.")
    parser.add_argument('--model', type=str, default='xgboost',
                        choices=['xgboost', 'lightgbm', 'random_forest', 'logistic'],
                        help='Model type to train')
    parser.add_argument('--symbol', type=str, default='BTCUSDT', help='Trading symbol')
    parser.add_argument('--days', type=int, default=30, help='Number of days of history to use')
    args = parser.parse_args()

    train(args.model, args.symbol, args.days)


if __name__ == "__main__":
    main()
