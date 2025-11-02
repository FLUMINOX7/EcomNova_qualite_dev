# EcomNova API - Backend Endpoints

Cette branche (`feature/api-endpoints`) contient l'implémentation complète des endpoints API REST pour EcomNova.

## ⚠️ Prérequis Important

**Python 3.11 ou 3.12 REQUIS** - FastAPI 0.95.2 et Pydantic 1.10.7 ne sont PAS compatibles avec Python 3.13+

### Solution rapide si vous avez Python 3.13:

```bash
# Installer Python 3.11 avec pyenv
pyenv install 3.11.10
pyenv local 3.11.10

# Recréer l'environnement virtuel
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Démarrage Rapide

```bash
# 1. Activer l'environnement virtuel
source .venv/bin/activate

# 2. Configurer la base de données (si pas déjà fait)
cd backend
python create_db.py
cd ..

# 3. Démarrer le serveur
python start_server.py
```

Le serveur sera accessible sur:
- API: http://localhost:8000
- Documentation interactive (Swagger): http://localhost:8000/docs
- Documentation alternative (ReDoc): http://localhost:8000/redoc

## 📋 Endpoints Implémentés

### Core (in‑memory) (`/core`)
Ces endpoints utilisent le domaine en mémoire défini dans `backend/core.py` (aucune persistance en base). Utile pour la démo, les tests et le prototypage.

- `POST /core/auth/register` — inscription (sessions en mémoire)
- `POST /core/auth/login` — connexion (retourne un token de session en mémoire)
- `GET  /core/auth/me` — informations de l'utilisateur courant
- `GET  /core/products` — liste des produits actifs (en mémoire)
- `POST /core/products` — créer un produit (en mémoire)
- `GET  /core/cart` — voir le panier
- `POST /core/cart/items` — ajouter un article au panier
- `POST /core/orders` — checkout (création commande à partir du panier)

Note: pour ces endpoints, le header d'auth attendu est `Authorization: Bearer <token_session>` où le token provient de `POST /core/auth/login`.

### Authentication (`/auth`)
- `POST /auth/register` - Inscription d'un nouvel utilisateur
- `POST /auth/login` - Connexion utilisateur (retourne JWT token)
- `GET /auth/me` - Récupérer les infos de l'utilisateur connecté

### Products (`/products`)
- `GET /products` - Liste tous les produits actifs
- `GET /products/{id}` - Détails d'un produit
- `POST /products` - Créer un produit (admin uniquement)
- `PUT /products/{id}` - Modifier un produit (admin uniquement)

### Cart (`/cart`)
- `GET /cart` - Récupérer le panier de l'utilisateur
- `POST /cart/items` - Ajouter un article au panier
- `PUT /cart/items/{id}` - Modifier la quantité d'un article
- `DELETE /cart/items/{id}` - Retirer un article du panier

### Orders (`/orders`)
- `GET /orders` - Liste des commandes de l'utilisateur
- `GET /orders/{id}` - Détails d'une commande
- `POST /orders` - Créer une commande depuis le panier
- `PUT /orders/{id}/status` - Mettre à jour le statut (admin uniquement)
- `GET /orders/admin/all` - Toutes les commandes (admin uniquement)

### System
- `GET /health` - Health check
- `GET /ping-db` - Test connexion base de données

## 🔐 Authentification

L'API utilise JWT (JSON Web Tokens) pour l'authentification.

### Workflow:
1. S'inscrire: `POST /auth/register`
2. Se connecter: `POST /auth/login` (retourne un `access_token`)
3. Utiliser le token dans les requêtes suivantes:
   ```
   Authorization: Bearer <access_token>
   ```

### Exemple avec curl:

```bash
# 1. S'inscrire
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "address": "123 Main St"
  }'

# 2. Se connecter
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }' | jq -r '.access_token')

# 3. Utiliser le token
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

## 🗂️ Structure du Code

```
backend/
├── app.py                 # Point d'entrée FastAPI
├── dependencies.py        # Dépendances (DB session)
├── db.py                  # Configuration base de données
├── models_sql.py          # Modèles SQLAlchemy
├── auth/
│   ├── jwt.py            # Gestion JWT et hashing
│   └── __init__.py
├── schemas/
│   ├── user.py           # Schemas Pydantic pour users
│   ├── product.py        # Schemas Pydantic pour products
│   ├── cart.py           # Schemas Pydantic pour cart
│   ├── order.py          # Schemas Pydantic pour orders
│   └── __init__.py
├── repositories/
│   ├── user.py           # Repository users
│   ├── product.py        # Repository products
│   ├── cart.py           # Repository cart
│   ├── order.py          # Repository orders
│   └── __init__.py
└── routers/
    ├── auth.py           # Routes authentication
    ├── products.py       # Routes products
    ├── cart.py           # Routes cart
    ├── orders.py         # Routes orders
  ├── core_integration.py # Routes Core en mémoire (/core)
    └── __init__.py
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Avec coverage
pytest --cov=backend

# Tests spécifiques
pytest tests/test_auth.py
```

## 📦 Dépendances

Voir `requirements.txt`:
- `fastapi` - Framework web
- `uvicorn` - Serveur ASGI
- `sqlalchemy` - ORM
- `pydantic` - Validation de données
- `python-jose` - JWT
- `passlib` - Hashing de mots de passe
- `psycopg2-binary` - Driver PostgreSQL

## 🔧 Configuration

Créer un fichier `backend/.env`:

```env
DATABASE_URL=postgresql://ecomnova_user:1234@localhost:5432/ecomnova
JWT_SECRET_KEY=your-secret-key-change-in-production
```

## 🐛 Dépannage

### Erreur Python 3.13
```
TypeError: ForwardRef._evaluate() missing 1 required keyword-only argument: 'recursive_guard'
```
→ Utiliser Python 3.11 ou 3.12 (voir section Prérequis)

### Erreur de connexion DB
```
sqlalchemy.exc.OperationalError: connection to server failed
```
→ Vérifier que PostgreSQL est démarré et que les identifiants dans `.env` sont corrects

### Import errors
```
ModuleNotFoundError: No module named 'jose'
```
→ Installer les dépendances: `pip install -r requirements.txt`

## 📝 Prochaines Étapes

- [ ] Tests d'intégration complets
- [ ] Rate limiting
- [ ] Pagination des listes
- [ ] Upload d'images produits
- [ ] Système de paiement (Stripe/PayPal)
- [ ] Notifications email
- [ ] WebSockets pour updates temps réel
