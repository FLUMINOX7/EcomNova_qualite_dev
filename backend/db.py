from __future__ import annotations
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import text

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/ecomnova"
)

Base = declarative_base()


def get_engine(url: str | None = None) -> AsyncEngine:
    return create_async_engine(url or DATABASE_URL, echo=False)


def get_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_session(session_maker: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session


async def ping_db(session: AsyncSession) -> bool:
    try:
        await session.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


async def init_models(engine: AsyncEngine):
    # Create tables if they don't exist (uses run_sync to invoke SQLAlchemy metadata.create_all)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
