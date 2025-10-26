from __future__ import annotations
import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncEngine
from .db import get_engine, get_session_maker, init_models, get_session, ping_db, DATABASE_URL
from sqlalchemy.ext.asyncio import AsyncSession

app = FastAPI(title="EcomNova API (dev)")


@app.on_event("startup")
async def startup_event():
    # Initialize engine and create tables if necessary
    app.state.engine = get_engine(os.environ.get("DATABASE_URL", DATABASE_URL))
    app.state.session_maker = get_session_maker(app.state.engine)
    try:
        await init_models(app.state.engine)
    except Exception:
        # In dev this may fail if DB not available; we'll let ping-db handle connectivity
        pass


@app.on_event("shutdown")
async def shutdown_event():
    engine: AsyncEngine = getattr(app.state, "engine", None)
    if engine is not None:
        await engine.dispose()


def get_db_session() -> AsyncSession:
    return Depends(lambda: get_session(app.state.session_maker))


@app.get("/health")
async def health():
    return {"ok": True}


@app.get("/ping-db")
async def pingdb(session: AsyncSession = Depends(lambda: get_session(app.state.session_maker))):
    # Try a lightweight db call
    async for s in session:
        ok = await ping_db(s)
        if not ok:
            raise HTTPException(status_code=503, detail="DB unavailable")
        return {"db": "ok"}
