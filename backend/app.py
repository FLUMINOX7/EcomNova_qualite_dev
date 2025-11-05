from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.db import init_models, ping_db
from backend.dependencies import _engine, init_db
from backend.routers import (auth, cart, core_integration, invoices, orders,
                             products, stats, threads)

# Create FastAPI app
app = FastAPI(
    title="EcomNova API",
    description="E-commerce REST API for EcomNova project",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(invoices.router)
app.include_router(threads.router)
app.include_router(stats.router)
app.include_router(core_integration.router)


@app.on_event("startup")
def startup_event():
    """Initialize database on startup"""
    init_db()
    # Ensure all SQLAlchemy models are created (idempotent)
    try:
        from backend.dependencies import _engine as engine

        if engine is not None:
            init_models(engine)
    except Exception:
        # Don't block app startup if model init fails; ping-db endpoint will reflect status
        pass


@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown"""
    if _engine is not None:
        try:
            _engine.dispose()
        except Exception:
            pass


@app.get("/health")
def health():
    """Health check endpoint"""
    return {"status": "ok", "service": "EcomNova API"}


@app.get("/ping-db")
def pingdb():
    """Database connectivity check"""
    if _engine is None:
        raise HTTPException(status_code=503, detail="DB not initialized")

    ok = ping_db(_engine)
    if not ok:
        raise HTTPException(status_code=503, detail="DB unavailable")
    return {"db": "ok"}
