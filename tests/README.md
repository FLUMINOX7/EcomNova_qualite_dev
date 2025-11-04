# Tests — EcomNova

Tests automatisés pour le backend et le frontend.

## 🧪 Lancer les Tests

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

### Frontend (vitest)

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

## 📊 Couverture

La couverture actuelle des tests :
- Backend: 44 tests passent ✅
- Frontend: 5 tests passent ✅

## 📚 Documentation

Voir [TESTS_README.md](./TESTS_README.md) pour la documentation complète des tests.
