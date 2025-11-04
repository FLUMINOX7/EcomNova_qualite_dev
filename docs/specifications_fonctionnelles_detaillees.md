# Spécifications Fonctionnelles Détaillées — EcomNova

## 1. Introduction

Le présent document décrit les **spécifications fonctionnelles détaillées (SFD)** du système e-commerce **EcomNova**.  
L’objectif est de définir, de manière technique et précise, le fonctionnement interne des entités, des flux métiers, et des cas d’utilisation.  

L’architecture logicielle repose sur une séparation claire entre :
- **Les modèles de données** (entités métiers)
- **Les dépôts (repositories)** pour la gestion des données
- **Les services métiers** encapsulant la logique fonctionnelle
- **Une couche applicative** (exploitable via FastAPI côté backend et React côté frontend)

---

## 2. Architecture générale

Le code Python met en œuvre une **architecture en couches** respectant les principes de la **Clean Architecture** :

- **Couche Modèle (Domain Layer)** : définit les entités métiers (`User`, `Product`, `Order`, etc.)
- **Couche Repository (Data Layer)** : assure la persistance en mémoire (mock pour prototypage)
- **Couche Service (Application Layer)** : implémente la logique métier (paiement, livraison, facturation, etc.)
- **Couche Présentation (Interface Layer)** : sera implémentée par FastAPI et React.

---

## 3. Modèles de données

### 3.1. Utilisateur (`User`)

Représente un client ou un administrateur.

| Champ | Type | Description |
|-------|------|-------------|
| id | str | Identifiant unique |
| email | str | Adresse email (unique) |
| password_hash | str | Hash du mot de passe |
| first_name | str | Prénom |
| last_name | str | Nom |
| address | str | Adresse de livraison |
| is_admin | bool | Vrai si administrateur |

#### Règles :
- Le mot de passe est stocké sous forme de hash (`sha256::`).
- L’email ne peut pas être modifié.
- Un utilisateur peut mettre à jour son profil via `update_profile()` (sauf email et mot de passe).

---

### 3.2. Produit (`Product`)

Représente un article vendable sur le site.

| Champ | Type | Description |
|-------|------|-------------|
| id | str | Identifiant unique |
| name | str | Nom du produit |
| description | str | Description |
| price_cents | int | Prix en centimes |
| stock_qty | int | Quantité en stock |
| active | bool | Produit visible ou non |

#### Règles :
- Un produit inactif ne peut pas être ajouté au panier.
- Le stock est réservé ou libéré lors des opérations de commande.

---

### 3.3. Panier (`Cart`)

Panier temporaire associé à un utilisateur.

| Champ | Type | Description |
|-------|------|-------------|
| user_id | str | Identifiant utilisateur |
| items | Dict[str, CartItem] | Produits ajoutés au panier |

**Opérations principales :**
- `add(product, qty)` : ajoute un produit si stock disponible.
- `remove(product_id, qty)` : retire partiellement ou totalement un produit.
- `total_cents(product_repo)` : calcule le total du panier.

---

### 3.4. Commande (`Order`)

Représente l’ensemble des produits commandés par un utilisateur.

| Champ | Type | Description |
|-------|------|-------------|
| id | str | Identifiant unique |
| user_id | str | Identifiant client |
| items | List[OrderItem] | Produits commandés |
| status | Enum[OrderStatus] | Statut de la commande |
| created_at | float | Date de création |
| validated_at, paid_at, ... | Optional[float] | Étapes de cycle de vie |
| delivery | Optional[Delivery] | Détails de livraison |
| invoice_id | Optional[str] | Référence facture |
| payment_id | Optional[str] | Référence paiement |

**Cycle de vie d’une commande :**
```
CREE → VALIDEE → PAYEE → EXPEDIEE → LIVREE
       ↘ ANNULEE → REMBOURSEE
```

---

### 3.5. Facture (`Invoice`)

Représente la facture générée après paiement.

| Champ | Type | Description |
|-------|------|-------------|
| id | str | Identifiant unique |
| order_id | str | Référence commande |
| user_id | str | Référence utilisateur |
| lines | List[InvoiceLine] | Détails des produits |
| total_cents | int | Total TTC |
| issued_at | float | Timestamp d’émission |

---

### 3.6. Paiement (`Payment`)

Gère la transaction financière associée à une commande.

| Champ | Type | Description |
|-------|------|-------------|
| id | str | Identifiant unique |
| order_id | str | Commande associée |
| user_id | str | Client payeur |
| amount_cents | int | Montant total |
| provider | str | Prestataire (CB, Stripe, etc.) |
| provider_ref | Optional[str] | Référence transaction |
| succeeded | bool | Statut du paiement |
| created_at | float | Date de création |

---

### 3.7. Livraison (`Delivery`)

Suivi logistique des commandes.

| Champ | Type | Description |
|-------|------|-------------|
| id | str | Identifiant unique |
| order_id | str | Commande concernée |
| carrier | str | Transporteur |
| tracking_number | str | Numéro de suivi |
| address | str | Adresse de livraison |
| status | str | Statut (PREPAREE, EN_COURS, LIVREE) |

---

### 3.8. Support client (`MessageThread`, `Message`)

Permet les échanges entre clients et support.

| Élément | Description |
|----------|-------------|
| `MessageThread` | Contient un sujet, un utilisateur, et une liste de messages |
| `Message` | Contient le contenu, l’auteur, la date |

---

## 4. Repositories

Chaque entité principale dispose d’un dépôt en mémoire simulant une base de données :

- `UserRepository` : gestion des utilisateurs.
- `ProductRepository` : gestion du catalogue et du stock.
- `CartRepository` : gestion des paniers.
- `OrderRepository` : gestion des commandes et de leur statut.
- `InvoiceRepository` : gestion des factures.
- `PaymentRepository` : gestion des paiements.
- `ThreadRepository` : gestion du support client.

---

## 5. Services

### 5.1. Authentification (`AuthService`)
- Inscription d’un utilisateur.
- Connexion et gestion de session (`SessionManager`).
- Vérification du hash de mot de passe.

### 5.2. Catalogue (`CatalogService`)
- Liste les produits actifs.
- Utilisé côté front (React) pour afficher le catalogue.

### 5.3. Panier (`CartService`)
- Ajout / retrait de produits.
- Calcul du total.
- Nettoyage automatique après validation de commande.

### 5.4. Commandes (`OrderService`)
Implémente le cœur métier :

#### Front-office :
- `checkout(user_id)` : transforme le panier en commande.
- `pay_by_card(order_id, ...)` : effectue le paiement simulé.
- `request_cancellation(order_id)` : annule la commande avant expédition.

#### Back-office (admin) :
- `backoffice_validate_order()` : valide la commande.
- `backoffice_ship_order()` : expédie la commande.
- `backoffice_mark_delivered()` : marque comme livrée.
- `backoffice_refund()` : rembourse la commande.

---

### 5.5. Facturation (`BillingService`)
- Génération de facture PDF simulée.
- Création d’objets `Invoice` avec lignes de facturation (`InvoiceLine`).

### 5.6. Livraison (`DeliveryService`)
- Prépare, expédie et marque la commande comme livrée.
- Génère un numéro de suivi aléatoire.

### 5.7. Support client (`CustomerService`)
- Permet à un utilisateur d’ouvrir un ticket (`MessageThread`).
- Le support peut répondre et clôturer un fil de discussion.

---

## 6. Scénarios fonctionnels

### 6.1. Parcours client
1. Le client s’inscrit et se connecte.
2. Il consulte le catalogue (`CatalogService`).
3. Il ajoute des produits au panier.
4. Il valide sa commande (`OrderService.checkout`).
5. Il effectue un paiement carte (`OrderService.pay_by_card`).
6. Il reçoit une facture électronique.
7. Il suit la livraison jusqu’à réception.

### 6.2. Parcours administrateur
1. Valide les commandes créées.
2. Gère l’expédition et la livraison.
3. Traite les remboursements ou annulations.
4. Gère les tickets de support client.

---

## 7. Technologies utilisées

- **Backend** : FastAPI — framework Python moderne, rapide et asynchrone, largement utilisé pour les APIs REST.  
- **Frontend** : React — bibliothèque JavaScript très populaire pour les interfaces dynamiques et réactives.  
- **Langage principal** : Python 3.12+  
- **Base de données simulée** : stockage en mémoire (Mock) — pourra être remplacée par PostgreSQL.  

---

## 8. Conclusion

Le système **EcomNova** repose sur une architecture claire, modulaire et extensible.  
Les spécifications détaillées assurent la traçabilité entre les besoins du cahier des charges et les implémentations Python, facilitant ainsi :
- les tests unitaires,
- la maintenance,
- et l’intégration continue (CI/CD).