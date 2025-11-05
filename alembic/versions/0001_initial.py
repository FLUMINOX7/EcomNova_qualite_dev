"""Initial migration: create core tables

This migration uses the project's metadata to create all tables.
"""

from alembic import op


def upgrade() -> None:
    # Import the application's Base & models to populate metadata
    import backend.models_sql  # noqa: F401
    from backend.db import Base

    # Use metadata.create_all against the migration connection
    conn = op.get_bind()
    Base.metadata.create_all(bind=conn)


def downgrade() -> None:
    import backend.models_sql  # noqa: F401
    from backend.db import Base

    conn = op.get_bind()
    Base.metadata.drop_all(bind=conn)
