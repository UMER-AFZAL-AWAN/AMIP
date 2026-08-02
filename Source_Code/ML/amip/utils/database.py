from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_engine(uri: str):
    return create_engine(uri)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
