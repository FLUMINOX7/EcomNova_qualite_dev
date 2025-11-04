# Spécifications Fonctionnelles Générales (SFG)
## Projet : Site e-commerce **EcomNova**

---

## 1. Objectif du document
Ce document décrit les **spécifications fonctionnelles générales** du projet de site e-commerce **EcomNova**, à partir du cahier des charges validé.  
Il définit les **grandes fonctions** du système et le **comportement attendu** du point de vue des utilisateurs.

---

## 2. Présentation générale du système
Le système à développer est une **plateforme web de commerce en ligne** composée de deux parties :
- un **backend FastAPI (Python)** assurant la logique métier, la gestion des données et la sécurité ;  
- un **frontend React (JavaScript)** pour l’affichage des interfaces, la navigation et les interactions avec les utilisateurs.  

Les objectifs principaux :
- permettre aux clients de consulter, commander et payer des produits en ligne,  
- permettre à l’administrateur de gérer le contenu, les produits et les commandes.  

---

## 3. Acteurs du système

| Acteur | Description | Exemples d’actions |
|---------|--------------|-------------------|
| **Visiteur** | Utilisateur non connecté consultant le site | Consulter le catalogue, rechercher un produit |
| **Client** | Utilisateur inscrit et connecté | Passer une commande, suivre ses achats |
| **Administrateur** | Gestionnaire du site | Gérer produits, commandes, utilisateurs |

---

## 4. Fonctionnalités principales

### 4.1. Accueil et navigation
- Page d’accueil avec promotions, nouveautés, et catégories.  
- Menu de navigation clair et intuitif.  
- Barre de recherche dynamique (connectée à l’API).  
- Accès rapide au panier et à la connexion.

### 4.2. Catalogue produits
- Affichage des produits (catégorie, tri, recherche).  
- Fiche produit détaillée (photo, prix, description, stock).  
- Ajout au panier depuis la fiche produit.  
- Côté admin : CRUD complet sur les produits.

### 4.3. Panier d’achat
- Gestion du panier côté frontend (React, via contexte ou Redux).  
- Mise à jour en temps réel des quantités et du prix total.  
- Synchronisation avec le backend via FastAPI.  
- Passage à la commande.

### 4.4. Commande et paiement
- Validation de commande (adresse, mode de livraison, paiement).  
- Intégration d’un paiement sécurisé (Stripe ou PayPal).  
- Confirmation automatique via e-mail (API backend).  
- Récapitulatif visible dans l’espace client.

### 4.5. Espace client
- Inscription / Connexion sécurisée (JWT ou OAuth2).  
- Historique de commandes.  
- Modification des informations personnelles.  

### 4.6. Interface d’administration
- Tableau de bord avec statistiques (ventes, clients, produits).  
- Gestion des produits (ajout, modification, suppression).  
- Suivi et traitement des commandes.  
- Gestion des utilisateurs (activation, suppression, rôles).

---

## 5. Cas d’utilisation (texte)

**Visiteur :**
- Consulter le catalogue
- Rechercher un produit
- Créer un compte
- Ajouter un produit au panier

**Client :**
- Se connecter
- Passer une commande
- Consulter son historique
- Modifier ses informations

**Administrateur :**
- Gérer les produits
- Gérer les commandes
- Gérer les utilisateurs

---

## 6. Données manipulées

| Type de données | Description | Exemple |
|------------------|-------------|----------|
| Produit | ID, nom, description, prix, stock, image | “T-shirt Nova Rouge – 19,90€” |
| Client | Nom, prénom, email, mot de passe, adresse | “Marie Durand, marie@mail.com” |
| Commande | ID, client, produits, montant, date, statut | “CMD#2025-012” |
| Panier | Liste temporaire des articles avant paiement | 2× produit A, 1× produit B |
| Paiement | ID transaction, montant, date, statut | “Stripe#20251019-001” |

---

## 7. Interfaces attendues
- **Frontend React** : interface web responsive, fluide et ergonomique.  
- **Backend FastAPI** : endpoints RESTful sécurisés (authentification, produits, commandes, paiements).  
- **Interface admin** : tableau de bord accessible via authentification.  
- **API extensible** : prévue pour intégration mobile ou autres services externes.

---

## 8. Règles de gestion principales
1. Un client doit être connecté pour passer commande.  
2. Un produit ne peut être commandé que s’il est en stock.  
3. Le panier est conservé pendant la session.  
4. Le paiement valide automatiquement la commande.  
5. FastAPI valide toutes les données entrantes (modèles Pydantic).  
6. React gère les erreurs d’API et affiche des messages adaptés.  
7. L’accès administrateur est restreint et sécurisé.

---

## 9. Contraintes et performances attendues
- Temps de chargement < 3 secondes.  
- Temps de réponse API < 500 ms.  
- Compatibilité mobile et tablette.  
- Respect du RGPD et des normes HTTPS.  
- Base de données cohérente et sécurisée.  

---

## 10. Livrables
- Schémas UML et wireframes.  
- Code React et FastAPI versionné sur GitHub.  
- Plan de tests fonctionnels et rapport de validation.  
- Documentation technique (API + architecture).  
- Documentation utilisateur.  

---

## 11. Validation
Document validé par :
- Le **client EcomNova** (validation du besoin),  
- Le **chef de projet** (validation de la faisabilité).  

**Fait par :** Équipe projet **EcomNova**  
**Date :** 19 octobre 2025
