# ✅ Configuration Complète - EcomNova Backend

## Résumé de l'installation

L'environnement Python 3.12 est maintenant configuré et le backend FastAPI fonctionne avec les endpoints **Core (en mémoire)** intégrés.

### Ce qui a été fait

1. ✅ **Configuration pyenv** - Python 3.12.7 installé et activé
2. ✅ **Environnement virtuel** - Recréé avec Python 3.12
3. ✅ **Mise à jour dépendances** - FastAPI 0.120.4, Pydantic 2.12.3, SQLAlchemy 2.0.44
4. ✅ **Intégration core.py** - Endpoints `/core/*` exposant le domaine en mémoire
5. ✅ **Tests flow complet** - register → login → products → cart → orders ✓

---

## 🚀 Démarrage Rapide

### 1. Activer l'environnement

```bash
cd /home/fluminox/Documents/School/BUT/BUT3/Qualite_Dev/EcomNova_qualite_dev
source .venv/bin/activate
```

### 2. Démarrer l'API

```bash
export DATABASE_URL='postgresql://ecomnova_user:1234@localhost:5432/ecomnova'
uvicorn backend.app:app --host 127.0.0.1 --port 8000 --reload
```

### 3. Accéder à la documentation

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc
- **Health check**: http://127.0.0.1:8000/health

---

## 📋 Endpoints Core (en mémoire)

Ces endpoints utilisent `backend/core.py` sans toucher à PostgreSQL. Parfaits pour les démos et tests rapides.

### Authentification

```bash
# Inscription
curl -X POST http://127.0.0.1:8000/core/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@test.com",
    "password": "secret123",
    "first_name": "John",
    "last_name": "Doe",
    "address": "123 Main St"
  }'

# Connexion (récupère le token)
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/core/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@test.com",
    "password": "secret123"
  }' | jq -r '.access_token')

# Info utilisateur
curl http://127.0.0.1:8000/core/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

### Produits

```bash
# Créer un produit
curl -X POST http://127.0.0.1:8000/core/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "T-Shirt Logo",
    "description": "Coton bio premium",
    "price_cents": 1999,
    "stock_qty": 100
  }'

# Lister les produits
curl http://127.0.0.1:8000/core/products
```

### Panier

```bash
# Ajouter au panier
curl -X POST http://127.0.0.1:8000/core/cart/items \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PRODUCT_ID_HERE",
    "quantity": 2
  }'

# Voir le panier
curl http://127.0.0.1:8000/core/cart \
  -H "Authorization: Bearer $TOKEN"
```

### Commandes

```bash
# Checkout (créer commande depuis le panier)
curl -X POST http://127.0.0.1:8000/core/orders \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🔧 Architecture du Code

```
backend/
├── app.py                    # Point d'entrée FastAPI (inclut core_integration)
├── core.py                   # Domaine métier en mémoire (User, Product, Cart, Order, Services)
├── core_runtime.py           # Singletons et wiring des services core
├── routers/
│   ├── core_integration.py   # 🆕 Endpoints /core/*
│   ├── auth.py               # Endpoints /auth (SQL)
│   ├── products.py           # Endpoints /products (SQL)
│   ├── cart.py               # Endpoints /cart (SQL)
│   └── orders.py             # Endpoints /orders (SQL)
├── models_sql.py             # Modèles SQLAlchemy (PostgreSQL)
├── schemas/                  # Schémas Pydantic
├── repositories/             # Repositories SQL
└── dependencies.py           # DB session provider
```

---

## 🧪 Flux Testé avec Succès

```
✅ POST /core/auth/register
  → User créé: fa6ca831-bc26-4c3d-a404-da6392fb239a

✅ POST /core/auth/login
  → Token: c51084dc-3fcc-41e0-bc7c-354289f8c959

✅ GET /core/auth/me
  → Infos user: Alice Martin

✅ POST /core/products
  → Produit créé: T-Shirt Logo (1999 centimes)

✅ GET /core/products
  → Liste: 1 produit actif

✅ POST /core/cart/items
  → Panier: 2× T-Shirt Logo = 3998 centimes

✅ GET /core/cart
  → Total: 39,98€

✅ POST /core/orders
  → Commande créée: d7b31fe7-43f8-4f73-82c6-805078a8c65b (statut: CREE)
```

---

## 🐍 Versions Installées

- **Python**: 3.12.7 (via pyenv)
- **FastAPI**: 0.120.4
- **Pydantic**: 2.12.3 (migration v1→v2 effectuée)
- **SQLAlchemy**: 2.0.44
- **Uvicorn**: 0.38.0

---

## 📝 Prochaines Étapes (Optionnel)

1. **Seed automatique** - Ajouter quelques produits démo au démarrage pour `/core`
2. **Endpoints admin** - Exposer validation/expédition/remboursement sous `/core/admin`
3. **Tests automatisés** - Pytest pour valider le flow complet
4. **CI/CD** - GitHub Actions pour lancer tests et build
5. **Frontend** - Connecter l'interface React/Vue aux endpoints

---

## 🎉 Statut Final

**✅ BACKEND FONCTIONNEL**

- Les endpoints SQL (`/auth`, `/products`, `/cart`, `/orders`) sont prêts
- Les endpoints Core (`/core/*`) sont testés et fonctionnent
- La documentation interactive est accessible sur `/docs`
- Le serveur démarre sans erreur avec Python 3.12

---

Pour toute question ou assistance supplémentaire, n'hésite pas!
