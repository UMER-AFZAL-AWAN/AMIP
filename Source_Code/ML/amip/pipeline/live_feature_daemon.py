import os
import sys
import time
import json
import logging
import pandas as pd
from datetime import datetime, timezone
from sqlalchemy import text

# Add the parent directory to the path so we can import amip
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from amip.utils.database import get_engine, get_session, MarketCandle, MarketFeature
from amip.features.feature_pipeline import FeaturePipeline

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DB_URI = "postgresql://amip_admin:amip_secure_2026@localhost:5432/amip_market_intelligence"
POLL_INTERVAL_SECONDS = 15

def get_latest_candles(session, symbol: str, limit: int = 100):
    """Fetch the latest candles for the given symbol to compute features."""
    candles = session.query(MarketCandle)\
                     .filter(MarketCandle.Symbol == symbol)\
                     .order_by(MarketCandle.CloseTime.desc())\
                     .limit(limit)\
                     .all()
    return list(reversed(candles)) # Return in chronological order

def run_daemon():
    logger.info("Starting Live Feature Daemon...")
    engine = get_engine(DB_URI)
    pipeline = FeaturePipeline()
    
    last_processed_time = None
    symbol = "BTCUSDT"

    while True:
        try:
            session = get_session(engine)
            
            # 1. Fetch the latest candles (need enough history for indicators like MA50)
            candles = get_latest_candles(session, symbol, limit=100)
            
            if not candles:
                logger.debug("No candles found yet. Waiting...")
                time.sleep(POLL_INTERVAL_SECONDS)
                session.close()
                continue
                
            latest_candle = candles[-1]
            
            # Check if we've already processed this candle
            if last_processed_time and latest_candle.CloseTime <= last_processed_time:
                logger.debug("No new candles. Waiting...")
                time.sleep(POLL_INTERVAL_SECONDS)
                session.close()
                continue
                
            logger.info(f"New candle detected! Processing CloseTime: {latest_candle.CloseTime}")
            
            # 2. Convert to DataFrame for FeaturePipeline
            df = pd.DataFrame([{
                'timestamp': c.CloseTime,
                'open': c.Open,
                'high': c.High,
                'low': c.Low,
                'close': c.Close,
                'volume': c.Volume
            } for c in candles])
            
            # 3. Transform data using the ML pipeline
            # Note: The FeaturePipeline drops NAs, so if we don't have enough history, it might return empty.
            features_df = pipeline.transform(df)
            
            if not features_df.empty:
                latest_features = features_df.iloc[-1]
                
                # We only want to save if the features correspond to the latest candle
                if latest_features['timestamp'] == latest_candle.CloseTime:
                    
                    # Convert row to dict, excluding timestamp for the JSON payload
                    feature_dict = latest_features.drop('timestamp').to_dict()
                    
                    # 4. Save to Database
                    new_feature = MarketFeature(
                        Symbol=symbol,
                        Timestamp=latest_candle.CloseTime,
                        FeatureDataJson=json.dumps(feature_dict)
                    )
                    
                    session.add(new_feature)
                    session.commit()
                    
                    logger.info(f"Successfully computed and saved {len(feature_dict)} features for {symbol}.")
                    last_processed_time = latest_candle.CloseTime
                else:
                    logger.warning("Computed features do not match latest candle time.")
            else:
                logger.warning(f"Not enough history to compute features. Need more candles. Current count: {len(candles)}")
                # Advance last_processed_time so we don't loop infinitely on the same insufficient data
                last_processed_time = latest_candle.CloseTime
                
            session.close()
            
        except Exception as e:
            logger.error(f"Error in daemon loop: {e}")
            
        time.sleep(POLL_INTERVAL_SECONDS)

if __name__ == "__main__":
    run_daemon()
