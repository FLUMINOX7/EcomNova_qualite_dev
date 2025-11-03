# EcomNova Frontend

> Interface utilisateur moderne pour EcomNova - E-commerce de technologies de pointe

## 🚀 Stack Technique

- **React 18** avec Vite (Fast Refresh, HMR)
- **React Router** pour la navigation
- **Context API** pour l'état global (Auth + Cart)
- **CSS moderne** avec thème galaxie bleu foncé
- **Fetch API** pour les appels backend

## 🎨 Design

Design galaxie futuriste avec :
- Fond bleu foncé avec animation d'étoiles
- Gradients cyan/violet pour les boutons
- Effets de glow et backdrop blur
- Responsive design

## 📦 Installation

```bash
cd frontend
npm install
```

## ⚙️ Configuration

Créer un fichier `.env` (optionnel) :

```env
VITE_API_URL=http://localhost:8000
```

Par défaut, l'app se connecte à `http://localhost:8000`

## 🏃 Lancer l'application

### Mode développement

```bash
npm run dev
```

L'application sera accessible sur **http://localhost:5173/**

### Build pour production

```bash
npm run build
npm run preview
```

## 🛠️ Structure du projet

```
frontend/
├── src/
│   ├── contexts/
│   │   ├── AuthContext.jsx      # Gestion auth (login, logout, token)
│   │   └── CartContext.jsx      # Gestion panier (add, remove, total)
│   ├── pages/
│   │   ├── Catalog.jsx          # Liste des produits
│   │   ├── Product.jsx          # Détail produit
│   │   ├── Cart.jsx             # Panier
│   │   ├── Checkout.jsx         # Finalisation commande
│   │   └── Auth.jsx             # Login/Register
│   ├── components/
│   │   └── ProductCard.jsx      # Carte produit réutilisable
│   ├── utils/
│   │   └── api.js               # Fonctions API (fetch, auth, cart)
│   ├── App.jsx                  # Composant racine + routing
│   ├── main.jsx                 # Point d'entrée
│   └── styles.css               # Styles globaux (thème galaxie)
└── public/
    └── assets/                   # Images statiques
```

## 🔑 Fonctionnalités

### ✅ Authentification
- Inscription avec email, mot de passe, nom, adresse
- Connexion avec JWT
- Token stocké dans localStorage
- Déconnexion

### ✅ Catalogue
- Affichage grille responsive des produits
- Ajout rapide au panier depuis la carte
- Navigation vers détail produit

### ✅ Produit
- Détails complets (nom, description, prix, stock)
- Sélection quantité
- Ajout au panier avec feedback

### ✅ Panier
- Affichage items avec quantités
- Modification quantité (+/-)
- Suppression items
- Calcul total automatique
- Sauvegarde dans localStorage

### ✅ Checkout
- Récapitulatif commande
- Informations livraison (depuis profil user)
- Confirmation et envoi au backend
- Vidage panier après succès

## 🔗 Intégration Backend

L'application utilise les endpoints `/core/*` du backend :

- `POST /core/register` - Inscription
- `POST /core/login` - Connexion
- `GET /core/cart` - Récupérer panier
- `POST /core/cart/add` - Ajouter au panier
- `POST /core/cart/remove` - Retirer du panier
- `POST /core/checkout` - Passer commande
- `GET /products` - Liste produits
- `GET /products/{id}` - Détail produit

## 🧪 Test du flux complet

1. **Lancer le backend** (dans un autre terminal) :
   ```bash
   cd backend
   python -m scripts.seed_products  # Ajouter produits démo
   uvicorn backend.app:app --reload
   ```

2. **Lancer le frontend** :
   ```bash
   cd frontend
   npm run dev
   ```

3. **Tester** :
   - Ouvrir http://localhost:5173
   - S'inscrire avec un nouveau compte
   - Parcourir le catalogue
   - Ajouter des produits au panier
   - Finaliser la commande

## 🎨 Personnalisation du thème

Les variables CSS sont définies dans `src/styles.css` :

```css
:root {
  --galaxy-dark: #0a0e27;
  --galaxy-deep: #1a1f3a;
  --galaxy-blue: #2d4a8e;
  --galaxy-bright: #4a7cff;
  --galaxy-cyan: #00d4ff;
  --galaxy-purple: #9333ea;
  /* ... */
}
```

## 📝 Notes

- Le panier est persisté dans `localStorage` (survit aux rechargements)
- Le token JWT est stocké dans `localStorage`
- Les images produits utilisent Unsplash (URLs dans seed_products.py)
- CORS est déjà configuré côté backend
