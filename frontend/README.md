# Frontend — EcomNova

Interface utilisateur moderne développée avec React 19, Vite 7 et React Router.

## 🚀 Démarrage Rapide (Docker)

```bash
# À la racine du projet
docker compose up --build

# Le frontend sera accessible sur http://localhost:8080
```

## 📋 Développement Local

### Prérequis

- Node.js 18+ et npm
- Backend API démarré sur http://localhost:8000

### Installation et lancement

```bash
cd frontend
npm install
npm run dev
```

Le frontend sera accessible sur http://localhost:5173

## 🧪 Tests

```bash
# Lancer les tests
npm test

# Tests en mode watch
npm test -- --watch

# Avec coverage
npm test -- --coverage
```

## 🏗️ Build Production

```bash
npm run build
```

Les fichiers optimisés seront dans `frontend/dist/`

## 📦 Technologies

- **React 19** - Framework UI
- **Vite 7** - Build tool & dev server
- **React Router 7** - Routing
- **Vitest** - Testing framework
- **Testing Library** - Tests composants

## 📚 Structure

```
frontend/
├── src/
│   ├── pages/          # Pages de l'application
│   ├── components/     # Composants réutilisables
│   ├── contexts/       # React Context (Auth, Cart, etc.)
│   ├── utils/          # Utilitaires (API client)
│   └── __tests__/      # Tests unitaires
├── public/             # Assets statiques
└── docker/             # Configuration nginx
```

## 🔗 Documentation Complète

Voir [FRONTEND_README.md](./FRONTEND_README.md) pour plus de détails.
