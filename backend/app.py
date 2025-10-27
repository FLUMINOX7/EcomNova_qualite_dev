from __future__ import annotations
import os
from fastapi import FastAPI, Depends, HTTPException
from .db import get_engine, get_session_maker, init_models, get_session, ping_db, DATABASE_URL
from sqlalchemy.orm import Session

app = FastAPI(title="EcomNova API (dev)")


@app.on_event("startup")
def startup_event():
    # Initialize engine and create tables if necessary
    app.state.engine = get_engine(os.environ.get("DATABASE_URL", DATABASE_URL))
    app.state.session_maker = get_session_maker(app.state.engine)
    try:
        init_models(app.state.engine)
    except Exception:
        # In dev this may fail if DB not available; we'll let ping-db handle connectivity
        pass


@app.on_event("shutdown")
def shutdown_event():
    engine = getattr(app.state, "engine", None)
    if engine is not None:
        try:
            engine.dispose()
        except Exception:
            pass


def get_db_session() -> Session:
    return Depends(lambda: next(get_session(app.state.session_maker)))


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/ping-db")
def pingdb():
    engine = app.state.engine
    ok = ping_db(engine)
    if not ok:
        raise HTTPException(status_code=503, detail="DB unavailable")
    return {"db": "ok"}
