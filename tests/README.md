# Tests - EcomNova

Tests automatisés pour le backend et le frontend.

## Lancer les tests

### Backend (pytest)

```bash
# À la racine du projet
source .venv/bin/activate
pytest

# Avec détails
pytest -v

# Tests spécifiques
pytest tests/test_auth_endpoints.py
pytest tests/test_product_endpoints.py
```

### Frontend (Vitest)

```bash
cd frontend
npm test
```

### Via Docker

```bash
# Tests backend dans le container
docker compose exec backend python -m pytest -v

# Avec coverage
docker compose exec backend python -m pytest --cov=backend
```

## Couverture

La couverture actuelle des tests :
- Backend: 44 tests passent ✅
- Frontend: 5 tests passent ✅

## Documentation

Cette page centralise les commandes de test. Les guides de démarrage détaillés se trouvent dans les README racine, backend et frontend.
