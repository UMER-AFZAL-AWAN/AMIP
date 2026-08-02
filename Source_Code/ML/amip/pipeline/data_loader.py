import pandas as pd
import sqlalchemy
from ..config import config
from ..utils.database import get_engine

class DataLoader:
    def __init__(self):
        self.engine = get_engine(config.DB_URI)
        
    def load_historical_data(self, symbol: str, timeframe: str, limit: int = 5000) -> pd.DataFrame:
        """Load historical price data from PostgreSQL."""
        query = f"""
            SELECT * FROM market_data 
            WHERE symbol = '{symbol}' AND timeframe = '{timeframe}'
            ORDER BY timestamp DESC
            LIMIT {limit}
        """
        try:
            df = pd.read_sql(query, self.engine)
            if not df.empty:
                df = df.sort_values('timestamp').reset_index(drop=True)
            return df
        except Exception as e:
            # Fallback for testing without DB
            print(f"Warning: DB connection failed ({e}). Returning empty DataFrame.")
            return pd.DataFrame(columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
