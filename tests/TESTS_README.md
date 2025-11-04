# Tests — EcomNova

Suite de tests automatisés pour valider les fonctionnalités du backend.

## 📋 Tests disponibles

### Tests d'intégration API (/core)
**Fichier**: `tests/test_api_core_integration.py`  
**20 tests** couvrant tous les endpoints Core (en mémoire):

#### Authentication (9 tests)
- ✅ Inscription utilisateur
- ✅ Inscription email dupliqué (erreur 400)
- ✅ Connexion réussie
- ✅ Connexion mot de passe incorrect (erreur 401)
- ✅ Connexion utilisateur inexistant (erreur 401)
- ✅ Récupération info utilisateur avec token
- ✅ Accès sans token (erreur 401)
- ✅ Accès avec token invalide (erreur 401)

#### Produits (3 tests)
- ✅ Liste produits (catalogue vide)
- ✅ Liste produits avec articles
- ✅ Création de produit

#### Panier (4 tests)
- ✅ Voir panier vide
- ✅ Ajouter article au panier
- ✅ Ajouter multiples fois (incrémente quantité)
- ✅ Panier nécessite authentification

#### Commandes (3 tests)
- ✅ Checkout avec articles
- ✅ Checkout panier vide (erreur 400)
- ✅ Panier vidé après checkout

#### Flow complet (1 test)
- ✅ Parcours e-commerce complet: register → login → produits → panier → commande

### Tests domaine métier
**Fichier**: `tests/test_core.py`  
**1 test** du domaine métier `backend/core.py`:
- ✅ Flow complet de commande (checkout, paiement, expédition, livraison)

## 🚀 Exécuter les tests

### Prérequis
```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Installer les dépendances de test (si pas déjà fait)
pip install pytest pytest-asyncio httpx
```

### Tous les tests
```bash
pytest
```

### Tests spécifiques
```bash
# Seulement les tests d'intégration API
pytest tests/test_api_core_integration.py

# Seulement les tests du domaine
pytest tests/test_core.py

# Un test spécifique
pytest tests/test_api_core_integration.py::TestCoreAuth::test_register_new_user
```

### Options utiles
```bash
# Mode verbose avec détails
pytest -v

# Arrêter au premier échec
pytest -x

# Exécuter les tests en parallèle (si pytest-xdist installé)
pytest -n auto

# Afficher la sortie des print
pytest -s
```

## 📊 Coverage (optionnel)

⚠️ **Note**: Coverage nécessite sqlite3 dans Python. Si votre installation pyenv n'a pas sqlite3, installez-le d'abord:

```bash
# Installer libsqlite3-dev
sudo apt-get install libsqlite3-dev

# Réinstaller Python 3.12 avec sqlite3
pyenv uninstall 3.12.7
pyenv install 3.12.7

# Recréer le venv
rm -rf .venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Puis lancer avec coverage:
```bash
# Coverage avec rapport terminal
pytest --cov=backend --cov-report=term-missing

# Coverage avec rapport HTML
pytest --cov=backend --cov-report=html
# Ouvrir htmlcov/index.html dans le navigateur
```

## 🏗️ Structure des tests

```
tests/
├── conftest.py                    # Fixtures partagées (TestClient, reset_core_state)
├── test_api_core_integration.py   # Tests endpoints /core (20 tests)
├── test_core.py                   # Tests domaine métier (1 test)
├── test_models_sql.py             # Tests modèles SQL
└── test_smoke.py                  # Tests de base
```

### Fixtures disponibles

#### `client`
TestClient FastAPI pour faire des requêtes HTTP dans les tests.

```python
def test_example(client):
    response = client.get("/health")
    assert response.status_code == 200
```

#### `reset_core_state` (auto)
Nettoie automatiquement les repositories en mémoire avant chaque test.

#### `sample_product`
Crée un produit de test dans le catalogue en mémoire.

```python
def test_with_product(client, sample_product):
    response = client.get("/core/products")
    assert len(response.json()) == 1
```

#### `registered_user`
Inscrit et authentifie un utilisateur de test, retourne `{user, token, credentials}`.

```python
def test_with_auth(client, registered_user):
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    response = client.get("/core/auth/me", headers=headers)
    assert response.status_code == 200
```

## ✍️ Écrire de nouveaux tests

### Exemple: Test d'un nouvel endpoint

```python
# tests/test_my_feature.py

def test_my_new_endpoint(client, registered_user):
    """Test description claire."""
    # Arrange
    headers = {"Authorization": f"Bearer {registered_user['token']}"}
    data = {"field": "value"}
    
    # Act
    response = client.post("/core/my-endpoint", json=data, headers=headers)
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert result["field"] == "value"
```

### Best practices
- ✅ Un test = une assertion principale
- ✅ Nom de test descriptif (`test_checkout_empty_cart_returns_400`)
- ✅ Pattern AAA: Arrange, Act, Assert
- ✅ Utiliser les fixtures pour la préparation
- ✅ Nettoyer l'état entre tests (auto avec `reset_core_state`)

## 🐛 Debug

### Test échoue?
```bash
# Mode verbose avec trace complète
pytest tests/test_api_core_integration.py::test_name -vv

# Afficher les prints
pytest -s

# Démarrer pdb au point d'échec
pytest --pdb
```

### Voir les warnings
```bash
pytest -W all
```

## 🎯 CI/CD

Pour intégrer dans un pipeline CI (GitHub Actions, GitLab CI, etc.):

```yaml
# Exemple .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - run: pip install -r requirements.txt
      - run: pytest
```

## 📈 Résultats actuels

```
✅ 21/21 tests passent
⏱️  Temps d'exécution: ~0.3s
📦 Couverture: À mesurer avec --cov (nécessite sqlite3)
```

## 🔜 Prochains tests à ajouter

- [ ] Tests des endpoints SQL (`/auth`, `/products`, `/cart`, `/orders`)
- [ ] Tests des repositories SQL
- [ ] Tests de performance (charge, stress)
- [ ] Tests de sécurité (injection, XSS, etc.)
- [ ] Tests E2E avec base de données de test

---

Pour toute question sur les tests, consulte la [documentation pytest](https://docs.pytest.org/).
