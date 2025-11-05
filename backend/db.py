from __future__ import annotations

import os
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/ecomnova"
)

Base = declarative_base()


def get_engine(url: str | None = None) -> Engine:
    return create_engine(url or DATABASE_URL, echo=False)


def get_session_maker(engine: Engine) -> sessionmaker:
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session(session_maker: sessionmaker) -> Generator[Session, None, None]:
    session = session_maker()
    try:
        yield session
    finally:
        session.close()


def ping_db(engine: Engine) -> bool:
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


def init_models(engine: Engine):
    # Create tables if they don't exist
    # Ensure models are imported so that metadata is populated
    try:
        import backend.models_sql  # noqa: F401
    except Exception:
        # If import fails, continue; create_all will run on whatever metadata exists
        pass
    Base.metadata.create_all(bind=engine)
