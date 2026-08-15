from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid
import datetime

Base = declarative_base()

class MarketCandle(Base):
    __tablename__ = 'MarketCandles'
    
    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Exchange = Column(Integer, nullable=False)
    Symbol = Column(String, nullable=False)
    Interval = Column(Integer, nullable=False)
    OpenTime = Column(DateTime(timezone=True), nullable=False)
    CloseTime = Column(DateTime(timezone=True), nullable=False)
    Open = Column(Float, nullable=False)
    High = Column(Float, nullable=False)
    Low = Column(Float, nullable=False)
    Close = Column(Float, nullable=False)
    Volume = Column(Float, nullable=False)

class MarketFeature(Base):
    __tablename__ = 'MarketFeatures'
    
    Id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    Symbol = Column(String, nullable=False)
    Timestamp = Column(DateTime(timezone=True), nullable=False)
    FeatureDataJson = Column(Text, nullable=False)

def get_engine(uri: str):
    return create_engine(uri)

def get_session(engine):
    Session = sessionmaker(bind=engine)
    return Session()
