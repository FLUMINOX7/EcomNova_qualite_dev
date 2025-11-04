# Frontend — EcomNova

Interface utilisateur moderne développée avec React 19, Vite 7 et les dernières technologies web.

## ✨ **Fonctionnalités**

- 🏠 **Homepage moderne** avec statistiques animées et design glassmorphism
- 🛍️ **Catalogue intelligent** avec recherche avancée et filtres
- 🛒 **Panier dynamique** avec gestion temps réel des quantités
- 💳 **Checkout sécurisé** avec validation de paiement
- 👤 **Authentification** complète avec JWT
- 📱 **Design responsive** pour tous les appareils
- ⚡ **Performance optimisée** avec lazy loading et optimisations Vite

## 🚀 Démarrage Rapide (Docker)

```bash
# À la racine du projet
docker compose up --build

# Le frontend sera accessible sur http://localhost:8080
```

## 📋 Développement Local

### Prérequis

- **Node.js 18+** et npm
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
# Lancer les tests (5 tests)
npm test

# Tests en mode watch
npm test -- --watch

# Avec coverage
npm test -- --coverage
```

**Tests actuels** :
- `ProductCard.test.jsx` - Affichage composant produit
- `Checkout.test.jsx` - Validation paiement et workflow
- `Auth.test.jsx` - Page d'authentification

## 🏗️ Build Production

```bash
npm run build
```

Les fichiers optimisés seront dans `frontend/dist/`

## 📦 Technologies

| Technologie | Version | Usage |
|-------------|---------|-------|
| **React** | 19 | Framework UI principal |
| **Vite** | 7 | Build tool ultra-rapide et HMR |
| **React Router** | 7 | Navigation SPA fluide |
| **Vitest** | Latest | Framework de test moderne |
| **Testing Library** | Latest | Tests composants React |

## 📚 Structure

```
frontend/
├── src/
│   ├── pages/              # Pages principales
│   │   ├── Home.jsx       # Page d'accueil avec stats
│   │   ├── Products.jsx   # Catalogue avec filtres
│   │   ├── Auth.jsx       # Connexion/Inscription
│   │   ├── Cart.jsx       # Panier d'achat
│   │   └── Checkout.jsx   # Processus de commande
│   ├── components/         # Composants réutilisables
│   │   ├── ProductCard.jsx
│   │   ├── Header.jsx
│   │   └── ...
│   ├── contexts/          # React Context (Auth, Cart, etc.)
│   │   ├── AuthContext.jsx
│   │   ├── CartContext.jsx
│   │   └── NotificationContext.jsx
│   ├── utils/             # Utilitaires
│   │   └── api.js         # Client API REST
│   └── __tests__/         # Tests unitaires (5 tests)
├── public/                # Assets statiques
├── docker/                # Configuration nginx
└── package.json           # Dépendances et scripts
```

## 🎨 **Pages Principales**

### 🏠 **Home.jsx**
- Statistiques en temps réel depuis `/stats` API
- Animations CSS modernes (slideIn, bounce, pulse)
- Design glassmorphism avec particules flottantes
- Hero section avec call-to-action

### 🛍️ **Products.jsx** 
- Catalogue complet avec grille responsive
- Recherche en temps réel
- Filtres par catégorie
- Tri par prix, nom, popularité

### 💳 **Checkout.jsx**
- Validation de formulaire avancée
- Simulation de paiement sécurisé
- Algorithme de Luhn pour validation cartes
- Gestion d'erreurs et succès

### 🛒 **Cart.jsx**
- Gestion dynamique des quantités
- Calcul automatique des totaux
- Synchronisation avec backend
- Workflow vers checkout

## 🔧 Configuration

### Variables d'environnement

```env
# .env.local
VITE_API_URL=http://localhost:8000
```

### Scripts disponibles

```bash
npm run dev          # Serveur de développement
npm run build        # Build de production
npm run preview      # Prévisualiser le build
npm test             # Lancer les tests
npm run test:ui      # Interface graphique des tests
npm run lint         # Vérification du code
```

## 🚀 **Optimisations**

- **Code splitting** automatique par page
- **Lazy loading** des composants lourds
- **Tree shaking** pour réduire la taille du bundle
- **Hot Module Replacement** pour développement rapide
- **Compression Gzip** en production
- **Cache busting** automatique

## 🔗 Documentation Complète

- [Guide API](../API_README.md) - Endpoints et authentification
- [Tests Report](../TESTS_REPORT.md) - Détails des tests frontend
- [Spécifications](../docs/) - Cahier des charges complet
