# Backend - EcomNova

Guide de configuration et démarrage du backend FastAPI avec PostgreSQL.

## Démarrage rapide (Docker recommandé)

```bash
# À la racine du projet
docker compose up --build

# Le backend sera accessible sur http://localhost:8000
# Documentation API: http://localhost:8000/docs
```

## Démarrage Local

### Prérequis

- **Python 3.11 ou 3.12** (Python 3.13+ non supporté actuellement)
- PostgreSQL 15+
- `pyenv` (recommandé pour gérer les versions Python)

### Installation

1. **Créer et activer un environnement virtuel**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Installer les dépendances**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. **Configurer la base de données**

```bash
# Créer un fichier backend/.env
echo 'DATABASE_URL=postgresql://ecomnova_user:1234@localhost:5432/ecomnova' > backend/.env
```

Ou avec Docker pour PostgreSQL :

```bash
docker run --name ecomnova-db \
  -e POSTGRES_USER=ecomnova_user \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=ecomnova \
  -p 5432:5432 \
  -d postgres:15
```

4. **Initialiser les tables**

```bash
cd backend
python create_db.py
```

5. **Lancer le serveur**

```bash
export DATABASE_URL='postgresql://ecomnova_user:1234@localhost:5432/ecomnova'
uvicorn backend.app:app --reload --port 8000
```

### Endpoints disponibles

- `GET /health` — Vérification du serveur
- `GET /ping-db` — Test de connexion DB
- `GET /docs` — Documentation interactive (Swagger)
- `GET /redoc` — Documentation alternative

## Tests

```bash
# Tous les tests
pytest

# Avec détails
pytest -v

# Tests backend uniquement
pytest tests/test_auth_endpoints.py tests/test_product_endpoints.py
```

## Architecture

```
backend/
├── app.py                 # Point d'entrée FastAPI
├── core.py                # Domaine métier (en mémoire)
├── models_sql.py          # Modèles SQLAlchemy
├── routers/               # Endpoints API
│   ├── auth.py           # Authentification
│   ├── products.py       # Produits
│   ├── cart.py           # Panier
│   └── orders.py         # Commandes
├── repositories/          # Accès données
├── schemas/               # Schémas Pydantic
└── auth/                  # JWT & sécurité
```

## Dépannage

### Erreur Python 3.13

```
TypeError: ForwardRef._evaluate() missing required argument
```

→ Installer Python 3.11 ou 3.12 avec pyenv :

```bash
pyenv install 3.11.10
pyenv local 3.11.10
```

### Erreur de connexion PostgreSQL

→ Vérifier que PostgreSQL est démarré :

```bash
# Linux
sudo systemctl status postgresql

# macOS
brew services list

# Docker
docker ps | grep postgres
```

## Documentation

- La documentation interactive de l'API est disponible via `/docs`
- Les spécifications du projet se trouvent dans le dossier [docs](../docs)
