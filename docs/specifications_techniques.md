# Spécifications Techniques — EcomNova

## 1. Introduction

Ce document décrit les **spécifications techniques (ST)** du projet e-commerce **EcomNova**.  
Il détaille l’architecture logicielle, les choix technologiques, les bases de données, et les API à implémenter.

Objectif : fournir aux développeurs toutes les informations techniques nécessaires pour démarrer le développement.

---

## 2. Architecture générale

### 2.1. Architecture logicielle

- **Backend** : FastAPI (Python 3.12+), architecture en couches :
  - **Domain Layer** : entités métiers (`User`, `Product`, `Order`, etc.)
  - **Repository Layer** : accès aux données (PostgreSQL via SQLAlchemy)
  - **Service Layer** : logique métier (paiement, livraison, facturation, etc.)
  - **API Layer** : routes REST pour frontend et API externes
- **Frontend** : React (TypeScript recommandé), composants modulaires, appels API via `fetch` ou `axios`
- **Base de données** : PostgreSQL, schéma relationnel normalisé
- **Tests** : pytest pour backend, jest/react-testing-library pour frontend

### 2.2. Diagramme d’architecture

```
Frontend (React)
       │
       ▼
API REST (FastAPI)
       │
       ▼
Services métiers (OrderService, CartService, BillingService, etc.)
       │
       ▼
Repositories (SQLAlchemy ORM)
       │
       ▼
PostgreSQL
```
---

## 3. Base de données (PostgreSQL)

### 3.1. Tables principales

#### Utilisateur (`users`)
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | UUID | PK |
| email | VARCHAR(255) | UNIQUE, NOT NULL |
| password_hash | VARCHAR(255) | NOT NULL |
| first_name | VARCHAR(100) | NOT NULL |
| last_name | VARCHAR(100) | NOT NULL |
| address | TEXT | NOT NULL |
| is_admin | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

#### Produit (`products`)
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | UUID | PK |
| name | VARCHAR(255) | NOT NULL |
| description | TEXT | |
| price_cents | INTEGER | NOT NULL |
| stock_qty | INTEGER | NOT NULL |
| active | BOOLEAN | DEFAULT TRUE |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

#### Panier (`cart_items`)
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | UUID | PK |
| user_id | UUID | FK -> users(id) |
| product_id | UUID | FK -> products(id) |
| quantity | INTEGER | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

#### Commande (`orders`)
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | UUID | PK |
| user_id | UUID | FK -> users(id) |
| status | VARCHAR(20) | ENUM('CREE','VALIDEE','PAYEE','EXPEDIEE','LIVREE','ANNULEE','REMBOURSEE') |
| created_at | TIMESTAMP | DEFAULT NOW() |
| validated_at | TIMESTAMP | NULLABLE |
| paid_at | TIMESTAMP | NULLABLE |
| shipped_at | TIMESTAMP | NULLABLE |
| delivered_at | TIMESTAMP | NULLABLE |
| cancelled_at | TIMESTAMP | NULLABLE |
| refunded_at | TIMESTAMP | NULLABLE |

#### Order Items (`order_items`)
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | UUID | PK |
| order_id | UUID | FK -> orders(id) |
| product_id | UUID | FK -> products(id) |
| name | VARCHAR(255) | NOT NULL |
| unit_price_cents | INTEGER | NOT NULL |
| quantity | INTEGER | NOT NULL |

#### Facture (`invoices`)
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | UUID | PK |
| order_id | UUID | FK -> orders(id) |
| user_id | UUID | FK -> users(id) |
| total_cents | INTEGER | NOT NULL |
| issued_at | TIMESTAMP | DEFAULT NOW() |

#### Paiement (`payments`)
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | UUID | PK |
| order_id | UUID | FK -> orders(id) |
| user_id | UUID | FK -> users(id) |
| amount_cents | INTEGER | NOT NULL |
| provider | VARCHAR(50) | NOT NULL |
| provider_ref | VARCHAR(255) | NULLABLE |
| succeeded | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMP | DEFAULT NOW() |

#### Livraison (`deliveries`)
| Colonne | Type | Contraintes |
|---------|------|-------------|
| id | UUID | PK |
| order_id | UUID | FK -> orders(id) |
| carrier | VARCHAR(100) | NOT NULL |
| tracking_number | VARCHAR(50) | NULLABLE |
| address | TEXT | NOT NULL |
| status | VARCHAR(20) | ENUM('PREPAREE','EN_COURS','LIVREE') |
| created_at | TIMESTAMP | DEFAULT NOW() |

#### Support client (`message_threads`, `messages`)
| Table | Colonnes principales |
|-------|--------------------|
| message_threads | id (UUID, PK), user_id (FK), subject (TEXT), order_id (FK, NULLABLE), closed (BOOLEAN), created_at, updated_at |
| messages | id (UUID, PK), thread_id (FK), author_user_id (FK, NULLABLE), body (TEXT), created_at |

---

## 4. API REST (FastAPI)

### 4.1. Authentification
- `POST /auth/register` : inscription
- `POST /auth/login` : connexion
- `POST /auth/logout` : déconnexion

### 4.2. Produits
- `GET /products` : liste produits actifs
- `GET /products/{id}` : détail produit

### 4.3. Panier
- `GET /cart` : voir panier
- `POST /cart/add` : ajouter produit
- `POST /cart/remove` : retirer produit
- `POST /cart/clear` : vider le panier

### 4.4. Commandes
- `POST /orders/checkout` : création commande
- `GET /orders` : lister commandes utilisateur
- `POST /orders/{id}/pay` : paiement carte

### 4.5. Backoffice (admin)
- `POST /admin/orders/{id}/validate` : valider commande
- `POST /admin/orders/{id}/ship` : expédier commande
- `POST /admin/orders/{id}/delivered` : marquer livrée
- `POST /admin/orders/{id}/refund` : rembourser commande

### 4.6. Support client
- `POST /threads/open` : ouvrir un fil
- `POST /threads/{id}/message` : poster message
- `POST /threads/{id}/close` : fermer fil

---

## 5. Sécurité

- Hashage des mots de passe avec `sha256::` (à remplacer par bcrypt/argon2 en prod)
- HTTPS obligatoire pour toutes les communications frontend-backend
- Vérification JWT/session token côté API pour sécuriser endpoints
- Permissions administrateur pour toutes les routes `/admin/*`

---

## 6. Tests

- **Backend** : pytest pour chaque service et repository
- **Frontend** : jest + react-testing-library pour composants et appels API
- **CI/CD** : GitHub Actions pour tests automatiques à chaque push/PR

---

## 7. Conclusion

Ces spécifications techniques assurent que le développement pourra commencer avec **une base solide**, en respectant la structure existante du code, PostgreSQL comme base de données, et les API nécessaires pour le frontend React.