# Backend — EcomNova

Ce README décrit comment lancer le backend localement, se connecter à la base PostgreSQL locale et exécuter les tests.

Contenu rapide
- Prérequis
- Création d'un environnement Python et installation
- Configuration de la base de données (variable d'environnement)
- Initialisation des tables
- Lancement de l'API
- Tests
- Dépannage et recommandations

## Prérequis

- Git
- Python 3.11 (recommandé). Le projet peut poser des problèmes avec Python 3.13 à cause de versions de Pydantic/FastAPI.
- PostgreSQL local ou Docker (base `ecomnova` créée, utilisateur `ecomnova_user`, mot de passe `1234` dans cet exemple)

Facultatif mais utile : `pyenv` pour gérer la version Python.

## Installation et configuration (rapide)

1. Cloner le dépôt et se positionner à la racine du projet.

```bash
git clone <REPO_URL>
cd EcomNova_qualite_dev
git checkout feature/fastapi-postgres
```

2. Créer et activer un virtualenv :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances :

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Remarque : `requirements.txt` utilise `pg8000` (pilote pure-Python) pour éviter d'installer `libpq`/`libpq-dev`.

## Configurer la connexion à PostgreSQL

Exemple (remplace si nécessaire) :

```bash
export DATABASE_URL='postgresql+pg8000://ecomnova_user:1234@localhost:5432/ecomnova'
```

Si tu préfères Docker pour la BDD :

```bash
docker run --name ecomnova-db -e POSTGRES_USER=ecomnova_user -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=ecomnova -p 5432:5432 -d postgres:15
```

## Initialiser les tables

Le projet contient la fonction `init_models` (SQLAlchemy) qui crée les tables nécessaires depuis les modèles.

```bash
source .venv/bin/activate
python -c "from backend.db import get_engine, init_models; import os; engine=get_engine(os.environ['DATABASE_URL']); init_models(engine); print('init OK')"
```

Si tu vois `init OK`, les tables ont été créées avec succès.

## Lancer l'API

```bash
export DATABASE_URL='postgresql+pg8000://ecomnova_user:1234@localhost:5432/ecomnova'
source .venv/bin/activate
uvicorn backend.app:app --reload --port 8000
```

Endpoints utiles (exemples) :
- GET /health — vérifie que le serveur tourne
- GET /ping-db — vérifie la connectivité à la DB

## Tests

Les tests unitaires sont exécutés avec `pytest` :

```bash
source .venv/bin/activate
pytest -q
```

Remarque : les tests présents dans `tests/test_core.py` testent le module en mémoire (`backend/core.py`) et ne nécessitent pas la base PostgreSQL.

## Dépannage rapide

- Erreur d'import FastAPI / Pydantic sous Python 3.13 : installe et utilise Python 3.11 (pyenv recommandé).
- Si `pip install -r requirements.txt` échoue pour un driver Postgres (ex: `psycopg2`), soit installe `libpq-dev` et utilise `psycopg2-binary`, soit garde `pg8000` (pure Python) comme le projet le propose.
- Si `uvicorn` ne démarre pas : vérifier la variable `DATABASE_URL`, que PostgreSQL tourne (`pg_isready` ou `systemctl status postgresql`) et les versions Python.

## Workflow recommandé pour contributions

- Branche `dev` : intégration continue
- Crée une branche par feature : `feature/auth`, `feature/orders`, `feature/api-fastapi`, etc.
- Prépare des PRs petites et testées ; ajoute des tests unitaires et, si possible, tests d'intégration pour les endpoints exposés.

## Prochaines étapes que je peux réaliser (sur demande)

- Ajouter endpoint `POST /users/register` + test d'intégration (avec DB)
- Migrer `UserRepository` et `ProductRepository` vers SQLAlchemy
- Ajouter Alembic pour gérer les migrations
- Préparer GitHub Actions CI pour exécuter tests et lint

---

Si tu veux, je pousse cette branche vers le remote et je crée un PR draft. Ou bien je commence par ajouter un endpoint d'auth (register) et son test ; dis-moi ta préférence.
## Configuration du backend (FastAPI) et connexion locale à PostgreSQL

Ce guide rapide explique comment préparer ton environnement local pour exécuter le backend FastAPI et le connecter à ta base PostgreSQL locale (`ecomnova`). Il couvre : installation Python (pyenv recommandé), création d'un virtualenv, installation des dépendances, initialisation des tables, lancement de l'API et commandes utiles (push/PR).

Important : le projet a été développé et testé avec Python 3.11. Si tu utilises Python 3.13, tu peux rencontrer des incompatibilités (Pydantic/FastAPI). Je recommande d'installer Python 3.11 via `pyenv`.

### 1) Pré-requis système

- Git
- PostgreSQL (ou Docker si tu préfères)
- `build-essential` / `gcc` (optionnel si tu utilises drivers natifs)

Sur Debian/Ubuntu, installe les prérequis utiles :

```bash
sudo apt update
sudo apt install -y build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev curl git
```

Si tu veux utiliser `psycopg2` (non requis dans la configuration actuelle), installe aussi :

```bash
sudo apt install -y libpq-dev
```

### 2) (Optionnel mais recommandé) Installer pyenv et Python 3.11

Si tu n'as pas Python 3.11, installe `pyenv` puis Python 3.11 :

```bash
# installer pyenv (si absent)
curl https://pyenv.run | bash
# suivre les instructions pour ajouter pyenv à ton shell (~/.bashrc ou ~/.profile)
exec $SHELL

# installer Python 3.11
pyenv install 3.11.18
pyenv local 3.11.18

# vérifier
python --version
```

### 3) Créer et activer un virtualenv

À la racine du projet :

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4) Installer les dépendances

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

> Note : le `requirements.txt` du projet utilise `pg8000` (pilote pure‑Python) pour éviter les problèmes de compilation de `psycopg2` sur certaines machines.

### 5) Configurer la variable d'environnement `DATABASE_URL`

Ton utilisateur et mot de passe locaux :

- DB : `ecomnova`
- USER : `ecomnova_user`
- PASSWORD : `1234`
- HÔTE : `localhost`
- PORT : `5432`

Exporte l'URL (shell courant) :

```bash
export DATABASE_URL='postgresql+pg8000://ecomnova_user:1234@localhost:5432/ecomnova'
```

Pour que la variable soit permanente, ajoute-la à `~/.profile` ou utilise un fichier `.env` (avec `python-dotenv`) selon ton flux.

### 6) Initialiser les tables SQLAlchemy (création automatique)

Le projet contient une fonction `init_models` qui crée les tables à partir des modèles SQLAlchemy.

```bash
source .venv/bin/activate
python -c "from backend.db import get_engine, init_models; import os; engine=get_engine(os.environ['DATABASE_URL']); init_models(engine); print('init OK')"
```

Si tu as un message `init OK`, c'est bon.

### 7) Lancer le serveur FastAPI (uvicorn)

```bash
export DATABASE_URL='postgresql+pg8000://ecomnova_user:1234@localhost:5432/ecomnova'
source .venv/bin/activate
uvicorn backend.app:app --reload --port 8000
```

Si tout va bien, l'API écoute sur `http://127.0.0.1:8000`.

### 8) Tester la connectivité DB

Endpoint disponible : `GET /ping-db` — renvoie `{"db":"ok"}` si la DB répond.

```bash
curl http://127.0.0.1:8000/ping-db
# -> {"db":"ok"}
```

Si `uvicorn` échoue à démarrer à cause d'une erreur Pydantic/FastAPI (ex : sous Python 3.13), utilise Python 3.11 (voir étape 2).

### 9) Exécuter les tests unitaires

Les tests utilisent `pytest` :

```bash
source .venv/bin/activate
pytest -q
```

Remarque : les tests actuels (`tests/test_core.py`) couvrent le module en mémoire (`backend/core.py`), ils ne nécessitent pas la BDD.

### 10) Docker alternative (Postgres)

Si tu préfères lancer Postgres en container Docker :

```bash
docker run --name ecomnova-db -e POSTGRES_USER=ecomnova_user -e POSTGRES_PASSWORD=1234 -e POSTGRES_DB=ecomnova -p 5432:5432 -d postgres:15
```

### 11) Pousser la branche et créer un PR

Si tu veux pousser les changements de la branche courante (`feature/fastapi-postgres`) :

```bash
git push -u origin feature/fastapi-postgres
# puis créer un PR sur GitHub via l'interface ou `gh` :
gh pr create --title "feat: fastapi + postgres skeleton" --body "Ajout du squelette FastAPI + SQLAlchemy pour connexion Postgres" --draft
```

### Notes et recommandations

- J'ai privilégié le pilote `pg8000` (pure Python) pour éviter l'installation de paquets systèmes. Si tu préfères `psycopg2`, installe `libpq-dev` puis remplace `pg8000` par `psycopg2-binary` dans `requirements.txt`.
- Pour la suite : je peux
  - ajouter des endpoints d'authentification (register/login),
  - migrer `UserRepository`/`ProductRepository` vers SQLAlchemy,
  - ajouter Alembic pour gérer les migrations,
  - préparer CI pour exécuter les tests et build.

Si tu veux, je peux maintenant :
- préparer un patch pour ajouter un endpoint `/users` (register) et son test d'intégration, ou
- créer le fichier de migration Alembic skeleton, ou
- pousser la branche et ouvrir un PR draft.
