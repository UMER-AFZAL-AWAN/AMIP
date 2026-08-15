import os
import sys

# Add the parent directory to the path so we can import amip
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from sqlalchemy import text
from amip.utils.database import get_engine, get_session

# Use the same connection string as the backend
DB_URI = "postgresql://amip_admin:amip_secure_2026@localhost:5432/amip_market_intelligence"

def verify_connection():
    try:
        print(f"Connecting to database at {DB_URI}...")
        engine = get_engine(DB_URI)
        session = get_session(engine)
        
        # Test connection by executing a simple query
        result = session.execute(text("SELECT 1")).scalar()
        print(f"Database connection successful! Test query returned: {result}")
        
        # Try to count candles if the table exists
        try:
            count = session.execute(text('SELECT COUNT(*) FROM "MarketCandles"')).scalar()
            print(f"Found {count} market candles in the database.")
        except Exception as e:
            print("Table 'MarketCandles' might not exist yet or is empty. Error:", str(e))
            
        session.close()
    except Exception as e:
        print(f"Failed to connect to database. Error: {e}")

if __name__ == "__main__":
    verify_connection()
