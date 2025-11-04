# EcomNova - Plateforme E-commerce Moderne

[![Tests](https://github.com/FLUMINOX7/EcomNova_qualite_dev/actions/workflows/test.yml/badge.svg)](https://github.com/FLUMINOX7/EcomNova_qualite_dev/actions/workflows/test.yml)
[![Code Quality](https://github.com/FLUMINOX7/EcomNova_qualite_dev/actions/workflows/lint.yml/badge.svg)](https://github.com/FLUMINOX7/EcomNova_qualite_dev/actions/workflows/lint.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![React 19](https://img.shields.io/badge/React-19-61DAFB.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688.svg)](https://fastapi.tiangolo.com)

**EcomNova** est une plateforme e-commerce complète et moderne, développée avec les dernières technologies web. Elle intègre un backend FastAPI robuste, un frontend React élégant, et suit les meilleures pratiques de développement et de qualité logicielle.

## ✨ **Fonctionnalités Principales**

- 🏠 **Page d'accueil interactive** avec statistiques en temps réel et animations
- 🛍️ **Catalogue produits** avec recherche avancée et filtrage
- 🛒 **Panier d'achat** dynamique avec gestion des quantités
- 👤 **Authentification sécurisée** avec JWT
- 📦 **Gestion des commandes** complète
- 📊 **Interface d'administration** pour la gestion des produits
- 🔄 **API REST complète** avec documentation interactive

## 🚀 **Démarrage Rapide**

### Prérequis
- **Docker** et **Docker Compose** (recommandé)
- Ou **Python 3.11+** et **Node.js 18+** pour l'installation locale

### Option 1 : Docker (Recommandé) 🐳

```bash
# 1. Cloner le projet
git clone https://github.com/FLUMINOX7/EcomNova_qualite_dev.git
cd EcomNova_qualite_dev

# 2. Lancer tous les services
docker compose up --build

# 3. Accéder aux services
# • Frontend: http://localhost:8080
# • Backend API: http://localhost:8000  
# • Documentation API: http://localhost:8000/docs
```

### Option 2 : Installation Locale

Voir les guides détaillés :
- [Backend Setup](backend/README.md) - Configuration FastAPI + PostgreSQL
- [Frontend Setup](frontend/README.md) - Configuration React + Vite

### 🌱 Données de démonstration

```bash
# Peupler la base avec des produits exemples
docker compose exec backend python scripts/seed_products.py
```

## 📋 Fonctionnalités

### API REST Complète
- 🔐 **Authentification JWT** - Sécurisation des endpoints
- 📦 **Gestion Produits** - CRUD complet avec interface admin
- 🛒 **Panier dynamique** - Ajout/modification/suppression en temps réel
- 📝 **Commandes** - Création et suivi complet des commandes
- 👤 **Gestion Utilisateurs** - Profils et historique personnel
- 📊 **Statistiques** - Métriques en temps réel pour le dashboard

### Interface Utilisateur Moderne
- 🏠 **Page d'accueil** avec animations et statistiques live
- 🛍️ **Catalogue** avec recherche avancée et filtres intelligents
- 💳 **Checkout** sécurisé avec validation de paiement
- 📱 **Design responsive** adaptatif mobile/desktop
- ⚡ **Performance optimisée** avec Vite et React 19

### Deux Modes de Fonctionnement
1. **Mode Production** (`/auth`, `/products`, `/cart`, `/orders`)  
   Persistance complète en PostgreSQL avec SQLAlchemy
   
2. **Mode Développement** (`/core/*`)  
   Domaine métier en mémoire pour prototypage rapide

## 🏗️ **Architecture**

```
EcomNova/
├── 🎨 frontend/                # React 19 + Vite 7
│   ├── src/pages/             
│   │   ├── Home.jsx           # Page d'accueil avec stats animées
│   │   ├── Products.jsx       # Catalogue avec filtres avancés
│   │   └── ...                # Auth, Cart, Checkout
│   ├── src/components/        # Composants réutilisables
│   └── src/__tests__/         # Tests Vitest (5 tests)
│
├── ⚡ backend/                 # FastAPI + SQLAlchemy
│   ├── app.py                 # Point d'entrée principal
│   ├── routers/               # Endpoints API REST
│   │   ├── auth.py           # JWT Authentication
│   │   ├── products.py       # CRUD Produits
│   │   ├── stats.py          # Statistiques temps réel
│   │   └── ...               # Cart, Orders
│   ├── models_sql.py         # Modèles SQLAlchemy
│   └── core.py               # Domaine métier (alternative)
│
├── 🧪 tests/                  # Tests Backend (28 tests)
│   ├── test_api_core_integration.py  # Tests API (20 tests)
│   ├── test_core.py          # Tests domaine métier
│   └── conftest.py           # Fixtures pytest
│
├── 📚 docs/                   # Spécifications projet
└── 🐳 docker-compose.yml     # Orchestration complète
```

## 🛠️ **Stack Technique**

| Composant | Technologie | Version | Description |
|-----------|------------|---------|-------------|
| **Frontend** | React | 19 | Interface utilisateur moderne et réactive |
| **Build Tool** | Vite | 7 | Dev server ultra-rapide et HMR |
| **Routing** | React Router | 7 | Navigation SPA fluide |
| **Backend** | FastAPI | 0.115.0 | API REST haute performance |
| **Database** | PostgreSQL | 15+ | Base de données relationnelle robuste |
| **ORM** | SQLAlchemy | 2.0.36 | Mapping objet-relationnel moderne |
| **Auth** | JWT | - | Authentification sécurisée stateless |
| **Validation** | Pydantic | 2.10.4 | Validation de données stricte |
| **Testing** | pytest + Vitest | - | Tests backend et frontend |
| **Container** | Docker Compose | - | Orchestration multi-services |
| **CI/CD** | GitHub Actions | - | Tests automatisés et qualité |

## 🧪 **Tests & Qualité**

```bash
# Tests Backend (28 tests) 
pytest                           # Tous les tests
pytest tests/test_api_core_integration.py  # Tests API (20 tests)

# Tests Frontend (5 tests)
cd frontend && npm test

# Qualité du code
ruff check .                     # Linting Python
black --check .                  # Formatage Python
```

**Couverture actuelle** : 33 tests total (28 backend + 5 frontend)

## 📚 **Documentation**

| Document | Description |
|----------|-------------|
| [API Documentation](http://localhost:8000/docs) | Documentation interactive des endpoints (Swagger) |
| [API Guide](API_README.md) | Guide complet des endpoints et authentification |
| [Backend Setup](backend/README.md) | Configuration FastAPI et base de données |
| [Frontend Setup](frontend/README.md) | Configuration React et développement |
| [Tests Guide](tests/TESTS_README.md) | Guide des tests et fixtures |
| [Spécifications](docs/) | Cahier des charges et spécifications fonctionnelles |

## 🔄 **CI/CD & Qualité**

Le projet utilise **GitHub Actions** pour assurer la qualité :

- ✅ **Tests automatiques** sur Python 3.11 & 3.12
- 📊 **Analyse qualité** avec ruff, black, isort  
- 🔍 **Vérification** sur chaque push et PR
- 📋 **Badges de statut** en temps réel

Tous les PR doivent passer les tests CI/CD avant merge.

## 🤝 **Contribuer**

1. **Fork** le projet
2. **Créer** une branche feature (`git checkout -b feature/amazing-feature`)
3. **Committer** les changements (`git commit -m 'feat: add amazing feature'`)
4. **Pousser** vers la branche (`git push origin feature/amazing-feature`)
5. **Ouvrir** une Pull Request

### Standards de qualité

- Code formaté avec **black** et **ruff**
- Tests passants à **100%**
- Documentation à jour
- Messages de commit conventionnels

## 📄 **Licence & Équipe**

**Projet académique** - BUT3 Informatique, parcours Qualité & Développement

Développé dans le cadre du module Qualité & Développement logiciel, ce projet illustre l'application des bonnes pratiques de développement moderne.

---

## 🚦 **Status du Projet**

- 🟢 **Backend API** : Fonctionnel et testé
- 🟢 **Frontend React** : Interface moderne et responsive  
- 🟢 **Base de données** : PostgreSQL avec persistance
- 🟢 **Tests** : 33 tests couvrant les fonctionnalités critiques
- 🟢 **CI/CD** : Pipeline automatisé opérationnel
- 🟢 **Documentation** : Complète et à jour

**Prêt pour la production** ✨
