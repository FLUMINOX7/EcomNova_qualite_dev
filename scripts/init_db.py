"""
Initialize database tables
"""

from sqlalchemy import inspect, text

from backend.db import init_models
from backend.dependencies import init_db

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    # Get the engine directly
    from backend.dependencies import _engine

    if _engine is None:
        raise RuntimeError("Engine not initialized")
    # Ensure base tables exist
    init_models(_engine)
    # Migration: add image_url column to products if missing
    inspector = inspect(_engine)
    cols = [c["name"] for c in inspector.get_columns("products")]
    if "image_url" not in cols:
        print("Adding image_url column to products...")
        with _engine.connect() as conn:
            conn.execute(text("ALTER TABLE products ADD COLUMN image_url TEXT"))
            conn.commit()
    print("✓ Database tables created successfully!")
