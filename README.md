# EcomNova - Qualité & Développement

[![Tests](https://github.com/FLUMINOX7/EcomNova_qualite_dev/actions/workflows/test.yml/badge.svg)](https://github.com/FLUMINOX7/EcomNova_qualite_dev/actions/workflows/test.yml)
[![Code Quality](https://github.com/FLUMINOX7/EcomNova_qualite_dev/actions/workflows/lint.yml/badge.svg)](https://github.com/FLUMINOX7/EcomNova_qualite_dev/actions/workflows/lint.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)

Plateforme e-commerce moderne développée avec FastAPI, intégrant les bonnes pratiques de développement et de qualité logicielle.

## 🚀 Démarrage Rapide

### Option 1 : Docker (Recommandé) 🐳

```bash
# Cloner le dépôt
git clone https://github.com/FLUMINOX7/EcomNova_qualite_dev.git
cd EcomNova_qualite_dev

# Lancer tous les services (DB + Backend + Frontend)
docker compose up --build

# Accéder aux services
# Frontend: http://localhost:8080
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

**Commandes utiles:**
```bash
# Lancer en arrière-plan
docker compose up -d

# Voir les logs
docker compose logs -f

# Arrêter les services
docker compose down

# Nettoyer complètement (⚠️ supprime les données)
docker compose down -v

# Seed la base avec des produits démo
docker compose exec backend python scripts/seed_products.py
```

### Option 2 : Installation Locale

```bash
# Installer Python 3.12 (recommandé)
pyenv install 3.12.7
pyenv local 3.12.7

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app:app --reload --port 8000

# Frontend (dans un autre terminal)
cd frontend
npm install
npm run dev
```

Accédez à la documentation interactive : [http://localhost:8000/docs](http://localhost:8000/docs)

## 📋 Fonctionnalités

### API REST Complète
- 🔐 **Authentification JWT** - Sécurisation des endpoints
- 📦 **Gestion Produits** - CRUD complet avec admin
- 🛒 **Panier** - Ajout/modification/suppression d'articles
- 📝 **Commandes** - Création et suivi des commandes
- 👤 **Gestion Utilisateurs** - Profils et historique

### Deux Modes de Fonctionnement
1. **Mode SQL** (`/auth`, `/products`, `/cart`, `/orders`)  
   Persistance en base PostgreSQL avec SQLAlchemy
   
2. **Mode Core** (`/core/*`)  
   Domaine métier en mémoire pour démos et tests rapides

## 🏗️ Architecture

```
EcomNova_qualite_dev/
├── backend/
│   ├── app.py                 # Application FastAPI
│   ├── core.py                # Domaine métier (en mémoire)
│   ├── core_runtime.py        # Wiring des services core
│   ├── models_sql.py          # Modèles SQLAlchemy
│   ├── routers/               # Endpoints API
│   │   ├── auth.py
│   │   ├── products.py
│   │   ├── cart.py
│   │   ├── orders.py
│   │   └── core_integration.py
│   ├── repositories/          # Accès données SQL
│   ├── schemas/               # Schémas Pydantic
│   └── auth/                  # JWT & sécurité
├── tests/
│   ├── conftest.py            # Fixtures pytest
│   ├── test_api_core_integration.py  # 20 tests endpoints
│   └── test_core.py           # Tests domaine
├── .github/workflows/         # CI/CD
│   ├── test.yml               # Tests automatisés
│   └── lint.yml               # Qualité du code
└── docs/                      # Documentation projet
```

## 🧪 Tests

```bash
# Lancer tous les tests
pytest

# Tests avec détails
pytest -v

# Tests spécifiques
pytest tests/test_api_core_integration.py

# Voir la documentation des tests
cat tests/TESTS_README.md
```

**Couverture actuelle**: 22/23 tests passent ✅

## 🛠️ Technologies

- **Backend**: FastAPI 0.115.0, Pydantic 2.10.4
- **Frontend**: React 19, Vite 7, React Router 7
- **Base de données**: PostgreSQL + SQLAlchemy 2.0.36
- **Auth**: JWT (python-jose), bcrypt
- **Tests**: pytest, httpx, Vitest, Testing Library
- **CI/CD**: GitHub Actions
- **Code Quality**: ruff, black, isort
- **Containerization**: Docker, Docker Compose

## 📚 Documentation

- **API**: [API_README.md](API_README.md) - Guide complet des endpoints
- **Backend**: [backend/README.md](backend/README.md) - Configuration et déploiement
- **Tests**: [tests/TESTS_README.md](tests/TESTS_README.md) - Guide testing
- **Setup**: [SETUP_COMPLETE.md](SETUP_COMPLETE.md) - Installation détaillée

## 🔄 CI/CD

Le projet utilise GitHub Actions pour :
- ✅ **Tests automatiques** sur Python 3.11 & 3.12
- 📊 **Analyse qualité** (ruff, black, isort)
- 🔍 **Vérification** sur chaque push et PR

Voir les workflows dans `.github/workflows/`

## 🤝 Contribuer

1. Fork le projet
2. Créer une branche feature (`git checkout -b feature/amazing-feature`)
3. Commit les changements (`git commit -m 'feat: add amazing feature'`)
4. Push vers la branche (`git push origin feature/amazing-feature`)
5. Ouvrir une Pull Request

Les PR doivent passer tous les tests CI/CD avant merge.

## 📄 Licence

Projet académique - BUT3 Qualité & Développement

## 👥 Équipe

Développé dans le cadre du BUT Informatique - parcours Qualité & Développement
