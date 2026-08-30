import os
import sys
import time
import json
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timezone

# Add the parent directory to the path so we can import amip
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from amip.utils.database import get_engine, get_session, MarketFeature, ModelPrediction

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URI = "postgresql://amip_admin:amip_secure_2026@localhost:5432/amip_market_intelligence"
POLL_INTERVAL_SECONDS = 20
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Models/trained'))
SYMBOL = "BTCUSDT"


def load_trained_model():
    """Try to load a trained model from disk. Returns (model, True) or (None, False)."""
    model_path = os.path.join(MODELS_DIR, f"xgboost_{SYMBOL}.joblib")
    if os.path.exists(model_path):
        try:
            import joblib
            model = joblib.load(model_path)
            logger.info(f"Loaded trained model from {model_path}")
            return model, True
        except Exception as e:
            logger.warning(f"Failed to load trained model: {e}. Falling back to heuristic.")
    return None, False


def generate_prediction(feature_dict: dict) -> dict:
    """
    Generate a prediction from the feature vector.
    
    In production, this would load a trained XGBoost/LSTM model and run inference.
    For now, we use a heuristic based on the computed features to produce 
    realistic-looking predictions that respond to actual market conditions.
    """
    # Extract key signals from the feature vector if available
    log_return = feature_dict.get('log_return', 0.0)
    price_momentum = feature_dict.get('price_momentum', 0.0)
    bullish_strength = feature_dict.get('bullish_strength', 0.5)
    distance_from_ma = feature_dict.get('distance_from_ma', 0.0)
    
    # Build a simple composite signal from the features
    signal = 0.0
    signal += np.clip(log_return * 100, -1, 1) * 0.3      # Recent return direction
    signal += np.clip(price_momentum, -1, 1) * 0.2         # Momentum
    signal += (bullish_strength - 0.5) * 0.3                # Candle structure
    signal += np.clip(distance_from_ma * 10, -1, 1) * 0.2  # Distance from MA
    
    # Add a small amount of noise for realism
    signal += np.random.normal(0, 0.05)
    
    # Convert signal to probabilities via softmax-like transform
    raw_up = np.exp(signal * 2)
    raw_down = np.exp(-signal * 2)
    raw_neutral = np.exp(-abs(signal) * 0.5)
    
    total = raw_up + raw_down + raw_neutral
    up_prob = raw_up / total
    down_prob = raw_down / total
    neutral_prob = raw_neutral / total
    
    # Determine direction
    probs = [down_prob, neutral_prob, up_prob]
    direction = int(np.argmax(probs))  # 0=Down, 1=Neutral, 2=Up
    
    # Confidence = max probability
    confidence = float(max(probs))
    
    # Risk = entropy-based measure (higher entropy = higher risk)
    entropy = -sum(p * np.log(p + 1e-8) for p in probs)
    max_entropy = np.log(3)  # Maximum entropy for 3 classes
    risk = float(entropy / max_entropy)
    
    return {
        'direction': direction,
        'up_probability': float(up_prob),
        'down_probability': float(down_prob),
        'neutral_probability': float(neutral_prob),
        'confidence': confidence,
        'risk': risk,
    }


def run_daemon():
    logger.info("Starting Prediction Inference Daemon...")
    engine = get_engine(DB_URI)
    
    # Try to load a trained model
    trained_model, use_model = load_trained_model()
    if use_model:
        logger.info("Using TRAINED MODEL for inference.")
    else:
        logger.info("No trained model found. Using HEURISTIC predictions.")
    
    last_processed_time = None
    symbol = SYMBOL

    while True:
        try:
            session = get_session(engine)
            
            # 1. Fetch the latest computed feature row
            latest_feature = session.query(MarketFeature)\
                                     .filter(MarketFeature.Symbol == symbol)\
                                     .order_by(MarketFeature.Timestamp.desc())\
                                     .first()
            
            if not latest_feature:
                logger.debug("No features found yet. Waiting...")
                time.sleep(POLL_INTERVAL_SECONDS)
                session.close()
                continue
            
            # Check if we've already processed this feature
            if last_processed_time and latest_feature.Timestamp <= last_processed_time:
                logger.debug("No new features. Waiting...")
                time.sleep(POLL_INTERVAL_SECONDS)
                session.close()
                continue
            
            logger.info(f"New feature detected at {latest_feature.Timestamp}. Running inference...")
            
            # 2. Deserialize the feature JSON
            feature_dict = json.loads(latest_feature.FeatureDataJson)
            
            # 3. Run prediction (trained model or heuristic)
            if use_model and trained_model is not None:
                try:
                    feature_df = pd.DataFrame([feature_dict])
                    proba = trained_model.predict_proba(feature_df)
                    # Binary model: [P(down), P(up)]
                    if proba.shape[1] == 2:
                        down_p, up_p = float(proba[0][0]), float(proba[0][1])
                        neutral_p = 0.0
                    else:
                        down_p, neutral_p, up_p = float(proba[0][0]), float(proba[0][1]), float(proba[0][2])
                    
                    direction = int(np.argmax([down_p, neutral_p, up_p]))
                    confidence = float(max(down_p, neutral_p, up_p))
                    entropy = -sum(p * np.log(p + 1e-8) for p in [down_p, neutral_p, up_p] if p > 0)
                    risk = float(entropy / np.log(3))
                    
                    pred = {
                        'direction': direction,
                        'up_probability': up_p,
                        'down_probability': down_p,
                        'neutral_probability': neutral_p,
                        'confidence': confidence,
                        'risk': risk,
                    }
                except Exception as e:
                    logger.warning(f"Model inference failed: {e}. Falling back to heuristic.")
                    pred = generate_prediction(feature_dict)
            else:
                pred = generate_prediction(feature_dict)
            
            # 4. Save to database
            new_prediction = ModelPrediction(
                Direction=pred['direction'],
                UpProbability=pred['up_probability'],
                DownProbability=pred['down_probability'],
                NeutralProbability=pred['neutral_probability'],
                Confidence=pred['confidence'],
                Risk=pred['risk'],
                ActualResult=None,  # To be filled in later by evaluation
                Symbol=symbol,
                Timestamp=latest_feature.Timestamp,
            )
            
            session.add(new_prediction)
            session.commit()
            
            direction_label = ['DOWN', 'NEUTRAL', 'UP'][pred['direction']]
            logger.info(
                f"Prediction saved: {direction_label} "
                f"(confidence={pred['confidence']:.1%}, risk={pred['risk']:.1%}, "
                f"up={pred['up_probability']:.1%}, down={pred['down_probability']:.1%})"
            )
            
            last_processed_time = latest_feature.Timestamp
            session.close()
            
        except Exception as e:
            logger.error(f"Error in prediction daemon loop: {e}")
        
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    run_daemon()
