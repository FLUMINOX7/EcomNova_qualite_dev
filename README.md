# EcomNova

EcomNova est une plateforme e-commerce développée avec FastAPI, React et PostgreSQL. Le projet couvre le parcours utilisateur principal, l'administration, les tests automatisés et le déploiement via Docker Compose.

## Fonctionnalités principales

- Page d'accueil avec indicateurs en temps réel
- Catalogue produits avec recherche et filtrage
- Panier d'achat dynamique avec gestion des quantités
- Authentification sécurisée avec JWT
- Gestion des commandes
- Interface d'administration pour la gestion des produits
- API REST documentée via OpenAPI

## Démarrage rapide

### Prérequis
- **Docker** et **Docker Compose** (recommandé)
- Ou **Python 3.11+** et **Node.js 18+** pour l'installation locale

### Option 1 : Docker (recommandé)

```bash
# 1. Cloner le projet
git clone https://github.com/FLUMINOX7/EcomNova_qualite_dev.git
cd EcomNova_qualite_dev

# 2. Lancer tous les services
docker compose up --build

# 3. Accéder aux services
# Frontend: http://localhost:8080
# Backend API: http://localhost:8000
# Documentation API: http://localhost:8000/docs
```

### Option 2 : Installation Locale

Voir les guides détaillés :
- [Backend Setup](backend/README.md) - Configuration FastAPI + PostgreSQL
- [Frontend Setup](frontend/README.md) - Configuration React + Vite

### Données de démonstration

```bash
# Peupler la base avec des produits exemples
docker compose exec backend python scripts/seed_products.py
```

## Fonctionnalités

### API REST complète
- Authentification JWT pour sécuriser les endpoints
- Gestion des produits avec CRUD complet
- Panier dynamique avec mise à jour en temps réel
- Création et suivi des commandes
- Gestion des utilisateurs et de leurs profils
- Statistiques en temps réel pour le tableau de bord

### Interface utilisateur
- Page d'accueil avec statistiques
- Catalogue avec recherche et filtres
- Parcours de commande sécurisé
- Interface responsive pour desktop et mobile
- Frontend optimisé avec Vite et React 19

### Modes de fonctionnement
1. **Mode Production** (`/auth`, `/products`, `/cart`, `/orders`)  
   Persistance complète en PostgreSQL avec SQLAlchemy
   
2. **Mode Développement** (`/core/*`)  
   Domaine métier en mémoire pour prototypage rapide

## Architecture

```
EcomNova/
├── frontend/                   # React 19 + Vite 7
│   ├── src/pages/             
│   │   ├── Home.jsx            # Page d'accueil
│   │   ├── Products.jsx        # Catalogue
│   │   └── ...                 # Auth, Cart, Checkout
│   ├── src/components/         # Composants réutilisables
│   └── src/__tests__/          # Tests Vitest
│
├── backend/                    # FastAPI + SQLAlchemy
│   ├── app.py                  # Point d'entrée principal
│   ├── routers/                # Endpoints API REST
│   │   ├── auth.py             # Authentification JWT
│   │   ├── products.py         # CRUD produits
│   │   ├── stats.py            # Statistiques
│   │   └── ...                 # Cart, orders
│   ├── models_sql.py           # Modèles SQLAlchemy
│   └── core.py                 # Domaine métier en mémoire
│
├── tests/                      # Tests backend
│   ├── test_api_core_integration.py  # Tests API
│   ├── test_core.py           # Tests domaine métier
│   └── conftest.py            # Fixtures pytest
│
├── docs/                       # Spécifications projet
└── docker-compose.yml          # Orchestration complète
```

## Stack technique

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

## Tests et qualité

```bash
# Tests backend
pytest                           # Tous les tests
pytest tests/test_api_core_integration.py

# Tests frontend
cd frontend && npm test

# Qualité du code
ruff check .                     # Linting Python
black --check .                  # Formatage Python
```

**Couverture actuelle** : 33 tests au total

## Documentation

| Document | Description |
|----------|-------------|
| [API Documentation](http://localhost:8000/docs) | Documentation interactive des endpoints |
| [Backend README](backend/README.md) | Configuration FastAPI et base de données |
| [Frontend README](frontend/README.md) | Configuration React et développement |
| [Tests README](tests/README.md) | Guide des tests et fixtures |
| [Spécifications](docs/) | Cahier des charges et spécifications |

## CI/CD et qualité

Le projet utilise **GitHub Actions** pour assurer la qualité :

- Tests automatiques sur Python 3.11 et 3.12
- Analyse qualité avec ruff, black et isort
- Vérification sur chaque push et pull request
- Badges de statut en temps réel

Tous les PR doivent passer les tests CI/CD avant merge.

## Contribuer

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

## Licence

**Projet académique** - BUT3 Informatique, Qualité de Développement

Le projet illustre l'application des bonnes pratiques de développement logiciel.

