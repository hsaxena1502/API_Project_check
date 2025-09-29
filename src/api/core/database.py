"""
Database configuration and session management.
"""
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from src.utils.config import Config as settings

# Database URL from config
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

# Create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Dependency function that yields database sessions.
    
    Yields:
        Session: A database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
