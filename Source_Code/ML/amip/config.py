import os

class Config:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "amip_market_intelligence")
    DB_USER = os.getenv("DB_USER", "amip_admin")
    DB_PASS = os.getenv("DB_PASS", "amip_secure_2026")

    DB_URI = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    MODEL_DIR = os.getenv("MODEL_DIR", os.path.join(os.path.dirname(__file__), "..", "saved_models"))

config = Config()
