# Guide de Test des Nouvelles Fonctionnalités

## 🚀 Accès à l'application

- **Frontend**: http://localhost:8080
- **Backend API**: http://localhost:8000
- **Documentation API**: http://localhost:8000/docs

---

## 📋 Fonctionnalités à Tester

### 1. 💳 Système de Paiement

#### Étapes de test :
1. **Connectez-vous** ou créez un compte utilisateur
2. **Ajoutez des produits au panier** (3-4 produits différents)
3. **Allez au checkout** via le bouton "Panier" dans la navigation
4. **Vérifiez les informations de commande** :
   - Liste des produits
   - Prix total
   - Adresse de livraison pré-remplie

5. **Testez la validation du formulaire de paiement** :
   - Nom sur la carte (obligatoire)
   - Numéro de carte (format 16 chiffres validé par algorithme de Luhn)
   - Date d'expiration (format MM/YY)
   - CVV (3 chiffres)

6. **Testez un paiement refusé** :
   - Utilisez une carte se terminant par `0000` (ex: `4242 4242 4242 0000`)
   - ❌ Vous devriez voir "Paiement refusé"

7. **Testez un paiement accepté** :
   - Utilisez n'importe quelle autre carte valide (ex: `4242 4242 4242 4242`)
   - ✅ Vous devriez voir "Commande payée avec succès !"
   - Le panier doit être vidé automatiquement

---

### 2. 📦 Gestion des Commandes (Vue Client)

#### Accès : Cliquez sur "Mes Commandes" dans la navigation

#### Étapes de test :
1. **Visualisation de la liste des commandes** :
   - Voir toutes vos commandes
   - Filtrage possible par statut (tous, en attente, validé, expédié, livré, annulé, remboursé)

2. **Statuts de commande** (avec code couleur) :
   - 🟡 **Pending** (en attente) - jaune
   - 🟢 **Validated** (validée) - vert
   - 🔵 **Shipped** (expédiée) - bleu
   - ✅ **Delivered** (livrée) - vert foncé
   - ❌ **Cancelled** (annulée) - rouge
   - 💰 **Refunded** (remboursée) - violet

3. **Détails d'une commande** :
   - Cliquez sur "Voir détails"
   - Vérifiez : liste des produits, quantités, prix unitaires, total
   - Si expédiée : numéro de suivi affiché

4. **Annulation de commande** :
   - Bouton "Annuler" disponible uniquement pour les commandes "Pending" ou "Validated"
   - Après annulation : statut passe à "Cancelled"
   - ⚠️ Le stock des produits est restauré automatiquement

---

### 3. 🧾 Factures

#### Accès : Via l'API ou en développant la fonctionnalité frontend

#### Test via API (http://localhost:8000/docs) :
1. **Créez une commande et payez-la** (voir section 1)
2. **Dans Swagger UI** :
   - Allez à `/orders` → GET `/orders`
   - Récupérez l'ID d'une commande payée
   - Allez à `/invoices` → GET `/invoices/{invoice_id}`
   - Vous devriez voir :
     - Numéro de facture (INV-XXXXXXXX)
     - Date d'émission
     - Montant total
     - Lignes de facture détaillées (produits, quantités, prix)

---

### 4. 🚚 Suivi de Livraison

#### Via l'interface Admin (voir section 6)

#### Test du workflow complet :
1. **Commande Pending** → Admin valide → **Validated**
2. **Validated** → Admin expédie (génère numéro de suivi) → **Shipped**
3. **Shipped** → Admin marque livrée → **Delivered**
4. Dans "Mes Commandes" (client), vérifiez que le numéro de suivi s'affiche

---

### 5. 💬 Support Client (Tickets de Support)

#### Accès : Cliquez sur "Support" dans la navigation

#### Création d'un ticket :
1. **Cliquez sur "Nouveau Ticket"**
2. **Remplissez le formulaire** :
   - Sujet (ex: "Problème de livraison")
   - Message détaillé
3. **Soumettez** → Le ticket apparaît dans la liste

#### Conversation dans un ticket :
1. **Ouvrez un ticket** (cliquez dessus)
2. **Ajoutez un message** en tant que client
3. **Visualisez** :
   - Messages clients (à gauche, fond blanc)
   - Messages support (à droite, fond bleu) - simulez via l'API
4. **Fermez le ticket** (bouton "Fermer le ticket")

#### Test de la réponse Admin (via API) :
1. Dans Swagger UI : `/threads` → GET `/threads` (avec admin token)
2. Récupérez un thread ID
3. POST `/threads/{thread_id}/admin-reply` avec un message
4. Rechargez la page Support → Vous verrez la réponse admin

---

### 6. 👨‍💼 Dashboard Admin

#### Accès : Cliquez sur "Admin" dans la navigation
⚠️ **Important** : Vous devez être connecté avec un compte admin

#### Création d'un compte admin :
**Option 1 - Via API (Swagger)** :
1. Allez sur http://localhost:8000/docs
2. POST `/auth/register` avec :
   ```json
   {
     "email": "admin@ecomnova.com",
     "password": "admin123",
     "first_name": "Admin",
     "last_name": "EcomNova",
     "address": "1 rue Admin\n75000 Paris",
     "is_admin": true
   }
   ```

**Option 2 - Via SQL** :
```bash
docker exec -it ecomnova-db psql -U postgres -d ecomnova
UPDATE users SET is_admin = true WHERE email = 'votre@email.com';
```

#### Fonctionnalités Admin à tester :

##### A. Dashboard général
- **Statistiques en temps réel** :
  - Nombre total de commandes
  - Commandes en attente
  - Commandes expédiées
  - Revenu total

##### B. Gestion des commandes
1. **Filtrage par statut** (tous, pending, validated, shipped, delivered, cancelled, refunded)

2. **Actions sur commande "Pending"** :
   - ✅ **Valider** → Statut passe à "Validated"

3. **Actions sur commande "Validated"** :
   - 📦 **Expédier** → Génère un numéro de suivi automatique
   - Statut passe à "Shipped"

4. **Actions sur commande "Shipped"** :
   - 🏠 **Marquer comme livrée** → Statut passe à "Delivered"

5. **Actions sur commande "Validated" ou "Shipped"** :
   - 💰 **Rembourser** → Statut passe à "Refunded"
   - ⚠️ Le stock est restauré automatiquement

##### C. Détails des commandes
- Cliquez sur "Voir détails"
- Informations complètes :
  - Client (nom, email)
  - Adresse de livraison
  - Liste des produits avec quantités
  - Statut de paiement
  - Numéro de suivi (si expédié)

---

## 🧪 Scénarios de Test Complets

### Scénario 1 : Parcours Client Complet (Commande Réussie)
1. ✅ Inscription/Connexion
2. ✅ Ajouter 3 produits au panier
3. ✅ Checkout avec carte valide (`4242 4242 4242 4242`)
4. ✅ Vérifier commande dans "Mes Commandes" (statut Pending)
5. ✅ (Admin) Valider la commande
6. ✅ (Client) Vérifier statut Validated
7. ✅ (Admin) Expédier avec numéro de suivi
8. ✅ (Client) Voir numéro de suivi dans commande
9. ✅ (Admin) Marquer comme livrée
10. ✅ (Client) Vérifier statut Delivered

### Scénario 2 : Paiement Refusé
1. ✅ Ajouter produits au panier
2. ✅ Checkout avec carte refusée (`4242 4242 4242 0000`)
3. ✅ Vérifier message d'erreur "Paiement refusé"
4. ✅ Panier reste plein
5. ✅ Réessayer avec carte valide

### Scénario 3 : Annulation de Commande
1. ✅ Créer une commande (Pending)
2. ✅ Aller dans "Mes Commandes"
3. ✅ Cliquer sur "Annuler"
4. ✅ Vérifier statut Cancelled
5. ✅ (Optionnel) Vérifier que le stock a été restauré

### Scénario 4 : Remboursement
1. ✅ (Admin) Valider une commande
2. ✅ (Admin) Cliquer sur "Rembourser"
3. ✅ Vérifier statut Refunded
4. ✅ (Client) Voir commande remboursée dans liste

### Scénario 5 : Support Client
1. ✅ (Client) Créer un ticket "Produit défectueux"
2. ✅ (Client) Ajouter un message de suivi
3. ✅ (Admin via API) Répondre au ticket
4. ✅ (Client) Voir réponse et fermer ticket

---

## 🔍 Points de Vérification Importants

### Backend
- ✅ Aucune erreur dans les logs Docker : `docker logs ecomnova-backend`
- ✅ Base de données mise à jour : nouvelles tables créées
- ✅ API répond correctement : http://localhost:8000/health

### Frontend
- ✅ Aucune erreur console navigateur (F12)
- ✅ Toutes les pages chargent correctement
- ✅ Navigation fluide entre pages

### Base de Données
Vérifiez les nouvelles tables :
```bash
docker exec -it ecomnova-db psql -U postgres -d ecomnova -c "\dt"
```
Nouvelles tables :
- `payments`
- `invoices`
- `invoice_lines`
- `deliveries`
- `message_threads`
- `messages`

---

## 🐛 Résolution de Problèmes

### Les conteneurs ne démarrent pas
```bash
docker compose down
docker compose up -d --build
```

### Erreur de connexion base de données
```bash
docker logs ecomnova-db
docker logs ecomnova-backend
```

### Frontend ne charge pas
```bash
docker logs ecomnova-frontend
# Vérifiez http://localhost:8080
```

### Je ne suis pas admin
```sql
docker exec -it ecomnova-db psql -U postgres -d ecomnova
UPDATE users SET is_admin = true WHERE email = 'votre@email.com';
\q
```

---

## 📊 Vérification via API (Swagger UI)

Accédez à http://localhost:8000/docs pour tester directement les endpoints :

### Nouveaux endpoints :
- **POST** `/orders/{order_id}/pay` - Payer une commande
- **POST** `/orders/{order_id}/cancel` - Annuler une commande
- **POST** `/orders/{order_id}/ship` - Expédier une commande
- **POST** `/orders/{order_id}/deliver` - Marquer comme livrée
- **POST** `/orders/{order_id}/refund` - Rembourser
- **GET** `/invoices/{invoice_id}` - Récupérer une facture
- **POST** `/threads` - Créer un ticket support
- **GET** `/threads` - Liste des tickets
- **GET** `/threads/{thread_id}` - Détails d'un ticket
- **POST** `/threads/{thread_id}/messages` - Ajouter un message
- **POST** `/threads/{thread_id}/admin-reply` - Réponse admin
- **POST** `/threads/{thread_id}/close` - Fermer un ticket

---

## ✅ Checklist de Test Complète

- [ ] Paiement avec carte valide
- [ ] Paiement avec carte invalide
- [ ] Visualisation liste commandes
- [ ] Filtrage commandes par statut
- [ ] Détails d'une commande
- [ ] Annulation commande (client)
- [ ] Dashboard admin accessible
- [ ] Statistiques admin correctes
- [ ] Validation commande (admin)
- [ ] Expédition avec numéro de suivi (admin)
- [ ] Livraison confirmée (admin)
- [ ] Remboursement (admin)
- [ ] Création ticket support (client)
- [ ] Conversation dans ticket (client)
- [ ] Réponse admin via API
- [ ] Fermeture ticket (client)
- [ ] Facture générée après paiement
- [ ] Numéro de suivi visible côté client

---

## 🎉 Toutes les fonctionnalités sont maintenant implémentées !

Bon test ! 🚀
