"""
EcomNova API Application
========================

Point d'entrée principal de l'API REST EcomNova.
Cette application FastAPI fournit tous les endpoints pour le e-commerce :
- Authentification et gestion des utilisateurs
- Catalogue de produits
- Gestion du panier
- Commandes et facturation
- Support client

Architecture:
- FastAPI avec middleware CORS
- Base de données PostgreSQL via SQLAlchemy
- Authentification JWT
- Structure modulaire avec routers séparés
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.db import init_models, ping_db
from backend.dependencies import _engine, init_db
from backend.routers import (auth, cart, core_integration, invoices, orders,
                             products, stats, threads)

# Création de l'application FastAPI avec métadonnées
app = FastAPI(
    title="EcomNova API",
    description="E-commerce REST API for EcomNova project",
    version="1.0.0",
    docs_url="/docs",  # Documentation Swagger UI
    redoc_url="/redoc",  # Documentation ReDoc
)

# Configuration du middleware CORS
# Permet les requêtes cross-origin pour le développement
# En production, spécifier les origines autorisées
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ En production: spécifier les domaines autorisés
    allow_credentials=True,  # Autorise les cookies/headers d'auth
    allow_methods=["*"],  # Toutes les méthodes HTTP autorisées
    allow_headers=["*"],  # Tous les headers autorisés
)

# Enregistrement des routeurs modulaires
# Chaque router gère un domaine fonctionnel spécifique
app.include_router(auth.router)  # Authentification et utilisateurs
app.include_router(products.router)  # Catalogue produits
app.include_router(cart.router)  # Gestion du panier
app.include_router(orders.router)  # Commandes et paiements
app.include_router(invoices.router)  # Facturation
app.include_router(threads.router)  # Support client
app.include_router(stats.router)  # Statistiques et métriques
app.include_router(core_integration.router)  # Endpoints core (in-memory)


@app.on_event("startup")
def startup_event():
    """
    Événement de démarrage de l'application.
    
    Initialise la base de données et crée les tables SQLAlchemy.
    Cette fonction est appelée automatiquement au démarrage de FastAPI.
    
    Note:
        Les erreurs d'initialisation ne bloquent pas le démarrage.
        L'endpoint /ping-db permet de vérifier l'état de la DB.
    """
    # Initialisation de la connexion à la base de données
    init_db()
    
    # Création des tables SQLAlchemy (opération idempotente)
    try:
        from backend.dependencies import _engine as engine

        if engine is not None:
            init_models(engine)
            print("✅ Database models initialized successfully")
    except Exception as e:
        # Ne pas bloquer le démarrage si l'init échoue
        print(f"⚠️  Database initialization failed: {e}")
        print("📡 Use /ping-db endpoint to check database status")


@app.on_event("shutdown")
def shutdown_event():
    """
    Événement d'arrêt de l'application.
    
    Nettoie les ressources et ferme proprement les connexions DB.
    Appelé automatiquement lors de l'arrêt de FastAPI.
    """
    if _engine is not None:
        try:
            _engine.dispose()
            print("✅ Database connections closed properly")
        except Exception as e:
            print(f"⚠️  Error during database cleanup: {e}")


@app.get("/health")
def health():
    """
    Endpoint de santé de l'application.
    
    Returns:
        dict: Status de l'API avec le nom du service
        
    Example:
        GET /health
        Response: {"status": "ok", "service": "EcomNova API"}
    """
    return {"status": "ok", "service": "EcomNova API"}


@app.get("/ping-db")
def pingdb():
    """
    Vérification de la connectivité à la base de données.
    
    Returns:
        dict: Status de la connexion DB
        
    Raises:
        HTTPException: 503 si la DB n'est pas initialisée ou indisponible
        
    Example:
        GET /ping-db
        Response: {"db": "ok"} ou erreur 503
    """
    if _engine is None:
        raise HTTPException(
            status_code=503, 
            detail="Database not initialized - check DATABASE_URL"
        )

    # Test de connectivité avec la base
    db_ok = ping_db(_engine)
    if not db_ok:
        raise HTTPException(
            status_code=503, 
            detail="Database unavailable - check connection"
        )
    
    return {"db": "ok"}
