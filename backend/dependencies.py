"""Database dependencies for FastAPI"""
from __future__ import annotations
import os
from typing import Generator
from sqlalchemy.orm import Session
from backend.db import get_engine, get_session_maker

# Global engine and session maker (initialized on startup)
_engine = None
_session_maker = None


def init_db():
    """Initialize database engine and session maker"""
    global _engine, _session_maker
    database_url = os.environ.get("DATABASE_URL", "postgresql://ecomnova_user:1234@localhost:5432/ecomnova")
    _engine = get_engine(database_url)
    _session_maker = get_session_maker(_engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session"""
    if _session_maker is None:
        init_db()
    
    session = _session_maker()
    try:
        yield session
    finally:
        session.close()
