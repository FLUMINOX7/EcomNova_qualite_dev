"""
EcomNova - Modèles métier et services e-commerce

Ce module constitue le cœur fonctionnel de l'application e-commerce EcomNova.
Il implémente une architecture Domain-Driven Design (DDD) avec :

- Modèles métier : User, Product, Order, Cart, Invoice, Payment, Delivery, etc.
- Repositories : Gestion de la persistance en mémoire des entités
- Services métier : AuthService, OrderService, CartService, BillingService, etc.
- Utilitaires : PasswordHasher, SessionManager, PaymentGateway

Architecture :
    ┌─ Models (dataclasses) : Entités métier
    ├─ Repositories : Accès aux données (pattern Repository)
    ├─ Services : Logique métier et orchestration
    └─ Utilities : Outils transversaux (hash, sessions, etc.)

Flux principal e-commerce :
    1. Authentification utilisateur (AuthService)
    2. Navigation catalogue (CatalogService)
    3. Gestion panier (CartService)
    4. Commande et paiement (OrderService + PaymentGateway)
    5. Facturation et livraison (BillingService + DeliveryService)
    6. Support client (CustomerService)

Note :
    Ce module est conçu pour fonctionner en mémoire (développement/tests).
    Pour la production, les repositories doivent être remplacés par des
    implémentations avec base de données (SQLAlchemy, etc.).

Auteur: EcomNova Team
Version: 1.0.0
"""

from __future__ import annotations

import hashlib
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto

# =========================
# ========== Models ======
# =========================


class OrderStatus(Enum):
    """
    Énumération des statuts possibles d'une commande.
    
    Cycle de vie d'une commande :
        CREE → VALIDEE → PAYEE → EXPEDIEE → LIVREE
        
    Chemins alternatifs :
        - ANNULEE : Annulation avant expédition
        - REMBOURSEE : Remboursement après paiement
    """
    CREE = auto()        # Commande créée, en attente de validation
    VALIDEE = auto()     # Validée par l'équipe (backoffice)
    PAYEE = auto()       # Paiement accepté et confirmé
    EXPEDIEE = auto()    # Colis expédié, tracking disponible
    LIVREE = auto()      # Livraison confirmée
    ANNULEE = auto()     # Commande annulée (avant expédition)
    REMBOURSEE = auto()  # Remboursement effectué


@dataclass
class User:
    """
    Modèle utilisateur de l'application.
    
    Représente un utilisateur client ou administrateur avec ses informations
    personnelles et ses droits d'accès.
    
    Attributes:
        id (str): Identifiant unique (UUID)
        email (str): Adresse email (identifiant de connexion)
        password_hash (str): Hash sécurisé du mot de passe
        first_name (str): Prénom
        last_name (str): Nom de famille
        address (str): Adresse de livraison
        is_admin (bool): Droits administrateur (False par défaut)
    """
    id: str
    email: str
    password_hash: str
    first_name: str
    last_name: str
    address: str
    is_admin: bool = False

    def update_profile(self, **fields):
        """
        Met à jour les informations du profil utilisateur.
        
        Seuls les champs modifiables sont acceptés (exclut id, email, 
        is_admin, password_hash pour la sécurité).
        
        Args:
            **fields: Champs à mettre à jour (first_name, last_name, address)
            
        Example:
            user.update_profile(first_name="Jean", address="Nouvelle adresse")
        """
        for k, v in fields.items():
            if hasattr(self, k) and k not in {
                "id",
                "email",
                "is_admin",
                "password_hash",
            }:
                setattr(self, k, v)


@dataclass
class Product:
    """
    Modèle produit du catalogue.
    
    Représente un article vendable avec ses caractéristiques,
    prix et gestion de stock.
    
    Attributes:
        id (str): Identifiant unique produit
        name (str): Nom commercial du produit
        description (str): Description détaillée
        price_cents (int): Prix en centimes (évite les erreurs de virgule flottante)
        stock_qty (int): Quantité en stock disponible
        active (bool): Produit actif/visible dans le catalogue
    """
    id: str
    name: str
    description: str
    price_cents: int  # Prix en centimes pour éviter les problèmes de float
    stock_qty: int
    active: bool = True


@dataclass
class CartItem:
    """
    Élément individuel dans un panier d'achat.
    
    Attributes:
        product_id (str): Référence vers le produit
        quantity (int): Quantité désirée
    """
    product_id: str
    quantity: int


@dataclass
class Cart:
    """
    Panier d'achat utilisateur.
    
    Gère les articles sélectionnés par un utilisateur avant commande.
    Inclut la validation des stocks et des prix.
    
    Attributes:
        user_id (str): Propriétaire du panier
        items (dict[str, CartItem]): Articles du panier (product_id -> CartItem)
    """
    user_id: str
    items: dict[str, CartItem] = field(default_factory=dict)  # key: product_id

    def add(self, product: Product, qty: int = 1):
        """
        Ajoute un produit au panier avec validation.
        
        Args:
            product (Product): Produit à ajouter
            qty (int): Quantité à ajouter (défaut: 1)
            
        Raises:
            ValueError: Si quantité invalide, produit inactif ou stock insuffisant
        """
        if qty <= 0:
            raise ValueError("Quantité invalide.")
        if not product.active:
            raise ValueError("Produit inactif.")
        if product.stock_qty < qty:
            raise ValueError("Stock insuffisant.")
        if product.id in self.items:
            self.items[product.id].quantity += qty
        else:
            self.items[product.id] = CartItem(product_id=product.id, quantity=qty)

    def remove(self, product_id: str, qty: int = 1):
        """
        Retire un produit du panier.
        
        Args:
            product_id (str): ID du produit à retirer
            qty (int): Quantité à retirer (0 = suppression complète)
        """
        if product_id not in self.items:
            return
        if qty <= 0:
            del self.items[product_id]
            return
        self.items[product_id].quantity -= qty
        if self.items[product_id].quantity <= 0:
            del self.items[product_id]

    def clear(self):
        """Vide complètement le panier."""
        self.items.clear()

    def total_cents(self, product_repo: ProductRepository) -> int:
        """
        Calcule le total du panier en centimes.
        
        Args:
            product_repo (ProductRepository): Repository pour récupérer les prix
            
        Returns:
            int: Total en centimes (produits inactifs exclus)
        """
        total = 0
        for it in self.items.values():
            p = product_repo.get(it.product_id)
            if p is None or not p.active:
                continue
            total += p.price_cents * it.quantity
        return total


@dataclass
class OrderItem:
    """
    Article d'une commande avec snapshot des données au moment de l'achat.
    
    Capture l'état du produit lors de la commande (nom, prix) pour préserver
    l'historique même si le produit évolue par la suite.
    
    Attributes:
        product_id (str): Référence vers le produit original
        name (str): Nom du produit au moment de l'achat
        unit_price_cents (int): Prix unitaire au moment de l'achat (centimes)
        quantity (int): Quantité commandée
    """
    product_id: str
    name: str
    unit_price_cents: int
    quantity: int


@dataclass
class InvoiceLine:
    """
    Ligne de facturation détaillée.
    
    Représente une ligne dans une facture avec calcul du total de ligne.
    
    Attributes:
        product_id (str): Référence produit
        name (str): Nom du produit facturé
        unit_price_cents (int): Prix unitaire en centimes
        quantity (int): Quantité facturée
        line_total_cents (int): Total de la ligne (unit_price * quantity)
    """
    product_id: str
    name: str
    unit_price_cents: int
    quantity: int
    line_total_cents: int


@dataclass
class Invoice:
    """
    Facture électronique.
    
    Document comptable généré après validation d'une commande.
    Inclut le détail des articles et le total facturé.
    
    Attributes:
        id (str): Numéro de facture unique
        order_id (str): Référence vers la commande
        user_id (str): Client facturé
        lines (list[InvoiceLine]): Lignes de facturation détaillées
        total_cents (int): Montant total facturé en centimes
        issued_at (float): Timestamp d'émission de la facture
    """
    id: str
    order_id: str
    user_id: str
    lines: list[InvoiceLine]
    total_cents: int
    issued_at: float  # epoch timestamp


@dataclass
class Payment:
    """
    Transaction de paiement.
    
    Enregistre les tentatives de paiement par carte bancaire avec
    référence du prestataire de paiement.
    
    Attributes:
        id (str): Identifiant unique du paiement
        order_id (str): Commande associée
        user_id (str): Utilisateur payeur
        amount_cents (int): Montant payé en centimes
        provider (str): Prestataire de paiement (ex: "CB", "PayPal")
        provider_ref (str | None): Référence de transaction du PSP
        succeeded (bool): Succès du paiement
        created_at (float): Timestamp de la tentative de paiement
    """
    id: str
    order_id: str
    user_id: str
    amount_cents: int
    provider: str  # ex: "CB"
    provider_ref: str | None
    succeeded: bool
    created_at: float


@dataclass
class Delivery:
    """
    Informations de livraison et suivi de colis.
    
    Gère l'expédition et le tracking des commandes avec transporteur.
    
    Attributes:
        id (str): Identifiant unique de livraison
        order_id (str): Commande à livrer
        carrier (str): Transporteur (ex: "POSTE", "UPS")
        tracking_number (str | None): Numéro de suivi du colis
        address (str): Adresse de livraison
        status (str): État de livraison ("PREPAREE", "EN_COURS", "LIVREE")
    """
    id: str
    order_id: str
    carrier: str
    tracking_number: str | None
    address: str
    status: str  # ex: "PREPAREE", "EN_COURS", "LIVREE"


@dataclass
class Message:
    """
    Message dans un fil de discussion support client.
    
    Attributes:
        id (str): Identifiant unique du message
        thread_id (str): Fil de discussion parent
        author_user_id (str | None): Auteur du message (None = agent support)
        body (str): Contenu du message
        created_at (float): Timestamp de création
    """
    id: str
    thread_id: str
    author_user_id: str | None  # None = agent support
    body: str
    created_at: float


@dataclass
class MessageThread:
    """
    Fil de discussion support client.
    
    Conversation entre un client et le support, optionnellement
    associée à une commande spécifique.
    
    Attributes:
        id (str): Identifiant unique du fil
        user_id (str): Client demandeur
        order_id (str | None): Commande associée (optionnel)
        subject (str): Sujet de la demande
        messages (list[Message]): Historique des messages
        closed (bool): Fil fermé par le support
    """
    id: str
    user_id: str
    order_id: str | None
    subject: str
    messages: list[Message] = field(default_factory=list)
    closed: bool = False


@dataclass
class Order:
    """
    Commande e-commerce complète.
    
    Entité centrale représentant une commande client avec son cycle de vie
    complet : création, validation, paiement, expédition, livraison.
    
    Attributes:
        id (str): Numéro de commande unique
        user_id (str): Client commandeur
        items (list[OrderItem]): Articles commandés avec snapshot des prix
        status (OrderStatus): État actuel de la commande
        created_at (float): Timestamp de création
        validated_at (float | None): Timestamp de validation (backoffice)
        paid_at (float | None): Timestamp de paiement confirmé
        shipped_at (float | None): Timestamp d'expédition
        delivered_at (float | None): Timestamp de livraison
        cancelled_at (float | None): Timestamp d'annulation
        refunded_at (float | None): Timestamp de remboursement
        delivery (Delivery | None): Informations de livraison
        invoice_id (str | None): Référence vers la facture
        payment_id (str | None): Référence vers le paiement
    """
    id: str
    user_id: str
    items: list[OrderItem]
    status: OrderStatus
    created_at: float
    validated_at: float | None = None
    paid_at: float | None = None
    shipped_at: float | None = None
    delivered_at: float | None = None
    cancelled_at: float | None = None
    refunded_at: float | None = None
    delivery: Delivery | None = None
    invoice_id: str | None = None
    payment_id: str | None = None

    def total_cents(self) -> int:
        """
        Calcule le montant total de la commande.
        
        Returns:
            int: Total en centimes basé sur les prix snapshot des OrderItem
        """
        return sum(i.unit_price_cents * i.quantity for i in self.items)


# =========================
# ===== Repositories ======
# =========================


class UserRepository:
    """
    Repository pour la gestion des utilisateurs.
    
    Implémentation en mémoire du pattern Repository pour les entités User.
    Fournit un accès rapide par ID et par email.
    
    Note:
        En production, cette classe devrait être remplacée par une
        implémentation avec base de données (SQLAlchemy, etc.)
    """
    
    def __init__(self):
        """Initialise les index en mémoire."""
        self._by_id: dict[str, User] = {}
        self._by_email: dict[str, User] = {}

    def add(self, user: User):
        """
        Ajoute un utilisateur au repository.
        
        Args:
            user (User): Utilisateur à ajouter
            
        Note:
            Met à jour automatiquement les deux index (ID et email)
        """
        self._by_id[user.id] = user
        self._by_email[user.email.lower()] = user

    def get(self, user_id: str) -> User | None:
        """
        Récupère un utilisateur par son ID.
        
        Args:
            user_id (str): Identifiant unique de l'utilisateur
            
        Returns:
            User | None: Utilisateur trouvé ou None
        """
        return self._by_id.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        """
        Récupère un utilisateur par son email (insensible à la casse).
        
        Args:
            email (str): Adresse email de l'utilisateur
            
        Returns:
            User | None: Utilisateur trouvé ou None
        """
        return self._by_email.get(email.lower())


class ProductRepository:
    """
    Repository pour la gestion du catalogue produits.
    
    Gère les produits avec accès par ID, filtrage par statut actif,
    et gestion automatique des stocks (réservation/libération).
    """
    
    def __init__(self):
        """Initialise l'index des produits."""
        self._by_id: dict[str, Product] = {}

    def add(self, product: Product):
        """
        Ajoute un produit au catalogue.
        
        Args:
            product (Product): Produit à ajouter
        """
        self._by_id[product.id] = product

    def get(self, product_id: str) -> Product | None:
        """
        Récupère un produit par son ID.
        
        Args:
            product_id (str): Identifiant unique du produit
            
        Returns:
            Product | None: Produit trouvé ou None
        """
        return self._by_id.get(product_id)

    def list_active(self) -> list[Product]:
        """
        Liste tous les produits actifs du catalogue.
        
        Returns:
            list[Product]: Produits avec active=True uniquement
        """
        return [p for p in self._by_id.values() if p.active]

    def reserve_stock(self, product_id: str, qty: int):
        """
        Réserve du stock pour une commande.
        
        Args:
            product_id (str): ID du produit
            qty (int): Quantité à réserver
            
        Raises:
            ValueError: Si stock insuffisant ou produit introuvable
        """
        p = self.get(product_id)
        if not p or p.stock_qty < qty:
            raise ValueError("Stock insuffisant.")
        p.stock_qty -= qty

    def release_stock(self, product_id: str, qty: int):
        """
        Libère du stock réservé (annulation, remboursement).
        
        Args:
            product_id (str): ID du produit
            qty (int): Quantité à libérer
        """
        p = self.get(product_id)
        if p:
            p.stock_qty += qty


class CartRepository:
    """
    Repository pour la gestion des paniers utilisateurs.
    
    Maintient un panier par utilisateur avec création automatique
    si nécessaire (pattern lazy initialization).
    """
    
    def __init__(self):
        """Initialise l'index des paniers par utilisateur."""
        self._by_user: dict[str, Cart] = {}

    def get_or_create(self, user_id: str) -> Cart:
        """
        Récupère ou crée le panier d'un utilisateur.
        
        Args:
            user_id (str): ID de l'utilisateur
            
        Returns:
            Cart: Panier existant ou nouvellement créé
        """
        if user_id not in self._by_user:
            self._by_user[user_id] = Cart(user_id=user_id)
        return self._by_user[user_id]

    def clear(self, user_id: str):
        """
        Vide le panier d'un utilisateur.
        
        Args:
            user_id (str): ID de l'utilisateur
        """
        self.get_or_create(user_id).clear()


class OrderRepository:
    """
    Repository pour la gestion des commandes.
    
    Maintient un index global par ID et un index par utilisateur
    pour permettre l'historique des commandes clients.
    """
    
    def __init__(self):
        """Initialise les index des commandes."""
        self._by_id: dict[str, Order] = {}
        self._by_user: dict[str, list[str]] = {}

    def add(self, order: Order):
        """
        Ajoute une commande au repository.
        
        Args:
            order (Order): Commande à ajouter
            
        Note:
            Met à jour automatiquement l'index utilisateur
        """
        self._by_id[order.id] = order
        self._by_user.setdefault(order.user_id, []).append(order.id)

    def get(self, order_id: str) -> Order | None:
        """
        Récupère une commande par son ID.
        
        Args:
            order_id (str): Numéro de commande
            
        Returns:
            Order | None: Commande trouvée ou None
        """
        return self._by_id.get(order_id)

    def list_by_user(self, user_id: str) -> list[Order]:
        """
        Récupère l'historique des commandes d'un utilisateur.
        
        Args:
            user_id (str): ID de l'utilisateur
            
        Returns:
            list[Order]: Liste des commandes de l'utilisateur
        """
        return [self._by_id[oid] for oid in self._by_user.get(user_id, [])]

    def update(self, order: Order):
        """
        Met à jour une commande existante.
        
        Args:
            order (Order): Commande modifiée
            
        Note:
            Utilisé pour les changements de statut, ajout de paiement, etc.
        """
        self._by_id[order.id] = order


class InvoiceRepository:
    """
    Repository pour la gestion des factures.
    
    Stockage simple des factures par ID pour consultation
    et archivage comptable.
    """
    
    def __init__(self):
        """Initialise l'index des factures."""
        self._by_id: dict[str, Invoice] = {}

    def add(self, invoice: Invoice):
        """
        Ajoute une facture au repository.
        
        Args:
            invoice (Invoice): Facture à archiver
        """
        self._by_id[invoice.id] = invoice

    def get(self, invoice_id: str) -> Invoice | None:
        """
        Récupère une facture par son ID.
        
        Args:
            invoice_id (str): Numéro de facture
            
        Returns:
            Invoice | None: Facture trouvée ou None
        """
        return self._by_id.get(invoice_id)


class PaymentRepository:
    """
    Repository pour la gestion des paiements.
    
    Archive toutes les tentatives de paiement (réussies ou échouées)
    pour audit et réconciliation financière.
    """
    
    def __init__(self):
        """Initialise l'index des paiements."""
        self._by_id: dict[str, Payment] = {}

    def add(self, payment: Payment):
        """
        Ajoute un paiement au repository.
        
        Args:
            payment (Payment): Transaction de paiement à archiver
        """
        self._by_id[payment.id] = payment

    def get(self, payment_id: str) -> Payment | None:
        """
        Récupère un paiement par son ID.
        
        Args:
            payment_id (str): Identifiant du paiement
            
        Returns:
            Payment | None: Paiement trouvé ou None
        """
        return self._by_id.get(payment_id)


class ThreadRepository:
    """
    Repository pour la gestion des fils de discussion support.
    
    Gère les conversations support client avec recherche par ID
    et par utilisateur pour l'historique du support.
    """
    
    def __init__(self):
        """Initialise l'index des fils de discussion."""
        self._by_id: dict[str, MessageThread] = {}

    def add(self, thread: MessageThread):
        """
        Ajoute un fil de discussion au repository.
        
        Args:
            thread (MessageThread): Fil de discussion à archiver
        """
        self._by_id[thread.id] = thread

    def get(self, thread_id: str) -> MessageThread | None:
        """
        Récupère un fil de discussion par son ID.
        
        Args:
            thread_id (str): Identifiant du fil
            
        Returns:
            MessageThread | None: Fil trouvé ou None
        """
        return self._by_id.get(thread_id)

    def list_by_user(self, user_id: str) -> list[MessageThread]:
        """
        Récupère tous les fils de discussion d'un utilisateur.
        
        Args:
            user_id (str): ID de l'utilisateur
            
        Returns:
            list[MessageThread]: Historique des demandes support
        """
        return [t for t in self._by_id.values() if t.user_id == user_id]


# =========================
# ===== Utilities ========
# =========================


class PasswordHasher:
    @staticmethod
    def hash(password: str) -> str:
        # Utiliser hashlib sha256 pour une valeur stable (remplacer par bcrypt/argon2 en production)
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    @staticmethod
    def verify(password: str, stored_hash: str) -> bool:
        return PasswordHasher.hash(password) == stored_hash


class SessionManager:
    """Gestion simple de sessions en mémoire."""

    def __init__(self):
        self._sessions: dict[str, str] = {}  # token -> user_id

    def create_session(self, user_id: str) -> str:
        token = str(uuid.uuid4())
        self._sessions[token] = user_id
        return token

    def destroy_session(self, token: str):
        self._sessions.pop(token, None)

    def get_user_id(self, token: str) -> str | None:
        return self._sessions.get(token)


# =========================
# ===== Services =========
# =========================


class AuthService:
    def __init__(self, users: UserRepository, sessions: SessionManager):
        self.users = users
        self.sessions = sessions

    def register(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        address: str,
        is_admin: bool = False,
    ) -> User:
        if self.users.get_by_email(email):
            raise ValueError("Email déjà utilisé.")
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            password_hash=PasswordHasher.hash(password),
            first_name=first_name,
            last_name=last_name,
            address=address,
            is_admin=is_admin,
        )
        self.users.add(user)
        return user

    def login(self, email: str, password: str) -> str:
        user = self.users.get_by_email(email)
        if not user or not PasswordHasher.verify(password, user.password_hash):
            raise ValueError("Identifiants invalides.")
        return self.sessions.create_session(user.id)

    def logout(self, token: str):
        self.sessions.destroy_session(token)


class CatalogService:
    def __init__(self, products: ProductRepository):
        self.products = products

    def list_products(self) -> list[Product]:
        return self.products.list_active()


class CartService:
    def __init__(self, carts: CartRepository, products: ProductRepository):
        self.carts = carts
        self.products = products

    def add_to_cart(self, user_id: str, product_id: str, qty: int = 1):
        product = self.products.get(product_id)
        if not product:
            raise ValueError("Produit introuvable.")
        self.carts.get_or_create(user_id).add(product, qty)

    def remove_from_cart(self, user_id: str, product_id: str, qty: int = 1):
        self.carts.get_or_create(user_id).remove(product_id, qty)

    def view_cart(self, user_id: str) -> Cart:
        return self.carts.get_or_create(user_id)

    def cart_total(self, user_id: str) -> int:
        return self.carts.get_or_create(user_id).total_cents(self.products)


class PaymentGateway:
    """Simulation d'un prestataire CB (à remplacer par Stripe/Adyen/etc.)."""

    def charge_card(
        self,
        card_number: str,
        exp_month: int,
        exp_year: int,
        cvc: str,
        amount_cents: int,
        idempotency_key: str,
    ) -> dict:
        # MOCK: succès si carte ne finit pas par '0000'
        ok = not card_number.endswith("0000")
        return {
            "success": ok,
            "transaction_id": str(uuid.uuid4()) if ok else None,
            "failure_reason": None if ok else "CARTE_REFUSEE",
        }

    def refund(self, transaction_id: str, amount_cents: int) -> dict:
        return {"success": True, "refund_id": str(uuid.uuid4())}


class BillingService:
    def __init__(self, invoices: InvoiceRepository):
        self.invoices = invoices

    def issue_invoice(self, order: Order) -> Invoice:
        lines = [
            InvoiceLine(
                product_id=i.product_id,
                name=i.name,
                unit_price_cents=i.unit_price_cents,
                quantity=i.quantity,
                line_total_cents=i.unit_price_cents * i.quantity,
            )
            for i in order.items
        ]
        inv = Invoice(
            id=str(uuid.uuid4()),
            order_id=order.id,
            user_id=order.user_id,
            lines=lines,
            total_cents=sum(l.line_total_cents for l in lines),
            issued_at=time.time(),
        )
        self.invoices.add(inv)
        return inv


class DeliveryService:
    def prepare_delivery(
        self, order: Order, address: str, carrier: str = "POSTE"
    ) -> Delivery:
        delivery = Delivery(
            id=str(uuid.uuid4()),
            order_id=order.id,
            carrier=carrier,
            tracking_number=None,
            address=address,
            status="PREPAREE",
        )
        return delivery

    def ship(self, delivery: Delivery) -> Delivery:
        delivery.status = "EN_COURS"
        delivery.tracking_number = (
            delivery.tracking_number or f"TRK-{uuid.uuid4().hex[:10].upper()}"
        )
        return delivery

    def mark_delivered(self, delivery: Delivery) -> Delivery:
        delivery.status = "LIVREE"
        return delivery


class OrderService:
    def __init__(
        self,
        orders: OrderRepository,
        products: ProductRepository,
        carts: CartRepository,
        payments: PaymentRepository,
        invoices: InvoiceRepository,
        billing: BillingService,
        delivery_svc: DeliveryService,
        gateway: PaymentGateway,
        users: UserRepository,
    ):
        self.orders = orders
        self.products = products
        self.carts = carts
        self.payments = payments
        self.invoices = invoices
        self.billing = billing
        self.delivery_svc = delivery_svc
        self.gateway = gateway
        self.users = users

    def checkout(self, user_id: str) -> Order:
        cart = self.carts.get_or_create(user_id)
        if not cart.items:
            raise ValueError("Panier vide.")
        # Réserver le stock
        order_items: list[OrderItem] = []
        for it in cart.items.values():
            p = self.products.get(it.product_id)
            if not p or not p.active:
                raise ValueError("Produit indisponible.")
            if p.stock_qty < it.quantity:
                raise ValueError(f"Stock insuffisant pour {p.name}.")
            self.products.reserve_stock(p.id, it.quantity)
            order_items.append(
                OrderItem(
                    product_id=p.id,
                    name=p.name,
                    unit_price_cents=p.price_cents,
                    quantity=it.quantity,
                )
            )
        order = Order(
            id=str(uuid.uuid4()),
            user_id=user_id,
            items=order_items,
            status=OrderStatus.CREE,
            created_at=time.time(),
        )
        self.orders.add(order)
        # vider le panier
        self.carts.clear(user_id)
        return order

    def pay_by_card(
        self, order_id: str, card_number: str, exp_month: int, exp_year: int, cvc: str
    ) -> Payment:
        order = self.orders.get(order_id)
        if not order:
            raise ValueError("Commande introuvable.")
        if order.status not in {OrderStatus.CREE, OrderStatus.VALIDEE}:
            raise ValueError("Statut de commande incompatible avec le paiement.")
        amount = order.total_cents()
        res = self.gateway.charge_card(
            card_number, exp_month, exp_year, cvc, amount, idempotency_key=order.id
        )
        payment = Payment(
            id=str(uuid.uuid4()),
            order_id=order.id,
            user_id=order.user_id,
            amount_cents=amount,
            provider="CB",
            provider_ref=res.get("transaction_id"),
            succeeded=res["success"],
            created_at=time.time(),
        )
        self.payments.add(payment)
        if not payment.succeeded:
            raise ValueError("Paiement refusé.")
        order.payment_id = payment.id
        order.status = OrderStatus.PAYEE
        order.paid_at = time.time()
        # Facture
        inv = self.billing.issue_invoice(order)
        order.invoice_id = inv.id
        self.orders.update(order)
        return payment

    def view_orders(self, user_id: str) -> list[Order]:
        return self.orders.list_by_user(user_id)

    def request_cancellation(self, user_id: str, order_id: str) -> Order:
        order = self.orders.get(order_id)
        if not order or order.user_id != user_id:
            raise ValueError("Commande introuvable.")
        if order.status in {OrderStatus.EXPEDIEE, OrderStatus.LIVREE}:
            raise ValueError("Trop tard pour annuler : commande expédiée.")
        order.status = OrderStatus.ANNULEE
        order.cancelled_at = time.time()
        # restituer le stock
        for it in order.items:
            self.products.release_stock(it.product_id, it.quantity)
        self.orders.update(order)
        return order

    def backoffice_validate_order(self, admin_user_id: str, order_id: str) -> Order:
        admin = self.users.get(admin_user_id)
        if not admin or not admin.is_admin:
            raise PermissionError("Droits insuffisants.")
        order = self.orders.get(order_id)
        if not order or order.status != OrderStatus.CREE:
            raise ValueError("Commande introuvable ou mauvais statut.")
        order.status = OrderStatus.VALIDEE
        order.validated_at = time.time()
        self.orders.update(order)
        return order

    def backoffice_ship_order(self, admin_user_id: str, order_id: str) -> Order:
        admin = self.users.get(admin_user_id)
        if not admin or not admin.is_admin:
            raise PermissionError("Droits insuffisants.")
        order = self.orders.get(order_id)
        if not order or order.status != OrderStatus.PAYEE:
            raise ValueError("La commande doit être payée pour être expédiée.")
        delivery = self.delivery_svc.prepare_delivery(
            order, address=self.users.get(order.user_id).address
        )
        delivery = self.delivery_svc.ship(delivery)
        order.delivery = delivery
        order.status = OrderStatus.EXPEDIEE
        order.shipped_at = time.time()
        self.orders.update(order)
        return order

    def backoffice_mark_delivered(self, admin_user_id: str, order_id: str) -> Order:
        admin = self.users.get(admin_user_id)
        if not admin or not admin.is_admin:
            raise PermissionError("Droits insuffisants.")
        order = self.orders.get(order_id)
        if not order or order.status != OrderStatus.EXPEDIEE or not order.delivery:
            raise ValueError("Commande non expédiée.")
        self.delivery_svc.mark_delivered(order.delivery)
        order.status = OrderStatus.LIVREE
        order.delivered_at = time.time()
        self.orders.update(order)
        return order

    def backoffice_refund(
        self, admin_user_id: str, order_id: str, amount_cents: int | None = None
    ) -> Order:
        admin = self.users.get(admin_user_id)
        if not admin or not admin.is_admin:
            raise PermissionError("Droits insuffisants.")
        order = self.orders.get(order_id)
        if not order or order.status not in {OrderStatus.PAYEE, OrderStatus.ANNULEE}:
            raise ValueError("Remboursement non autorisé au statut actuel.")
        amount = amount_cents or order.total_cents()
        # remboursement via le PSP mock
        payment = self.payments.get(order.payment_id) if order.payment_id else None
        if not payment or not payment.provider_ref:
            raise ValueError("Aucun paiement initial.")
        self.gateway.refund(payment.provider_ref, amount)
        order.status = OrderStatus.REMBOURSEE
        order.refunded_at = time.time()
        # restituer le stock si besoin
        for it in order.items:
            self.products.release_stock(it.product_id, it.quantity)
        self.orders.update(order)
        return order


class CustomerService:
    """Service client: fils de discussion & messages côté UI + réponses agents."""

    def __init__(self, threads: ThreadRepository, users: UserRepository):
        self.threads = threads
        self.users = users

    def open_thread(
        self, user_id: str, subject: str, order_id: str | None = None
    ) -> MessageThread:
        th = MessageThread(
            id=str(uuid.uuid4()), user_id=user_id, order_id=order_id, subject=subject
        )
        self.threads.add(th)
        return th

    def post_message(
        self, thread_id: str, author_user_id: str | None, body: str
    ) -> Message:
        th = self.threads.get(thread_id)
        if not th or th.closed:
            raise ValueError("Fil introuvable ou fermé.")
        if author_user_id is not None and not self.users.get(author_user_id):
            raise ValueError("Auteur inconnu.")
        msg = Message(
            id=str(uuid.uuid4()),
            thread_id=thread_id,
            author_user_id=author_user_id,
            body=body,
            created_at=time.time(),
        )
        th.messages.append(msg)
        return msg

    def close_thread(self, thread_id: str, admin_user_id: str):
        admin = self.users.get(admin_user_id)
        if not admin or not admin.is_admin:
            raise PermissionError("Droits insuffisants.")
        th = self.threads.get(thread_id)
        if not th:
            raise ValueError("Fil introuvable.")
        th.closed = True
        return th


# =========================
# ===== Demo / main =======
# =========================

if __name__ == "__main__":
    # Repos & services
    users = UserRepository()
    products = ProductRepository()
    carts = CartRepository()
    orders = OrderRepository()
    invoices = InvoiceRepository()
    payments = PaymentRepository()
    threads = ThreadRepository()
    sessions = SessionManager()

    auth = AuthService(users, sessions)
    catalog = CatalogService(products)
    cart_svc = CartService(carts, products)
    billing = BillingService(invoices)
    delivery_svc = DeliveryService()
    gateway = PaymentGateway()
    order_svc = OrderService(
        orders,
        products,
        carts,
        payments,
        invoices,
        billing,
        delivery_svc,
        gateway,
        users,
    )
    cs = CustomerService(threads, users)

    # Seed products
    p1 = Product(
        id=str(uuid.uuid4()),
        name="T-Shirt Logo",
        description="Coton bio",
        price_cents=1999,
        stock_qty=100,
    )
    p2 = Product(
        id=str(uuid.uuid4()),
        name="Sweat Capuche",
        description="Molleton",
        price_cents=4999,
        stock_qty=50,
    )
    products.add(p1)
    products.add(p2)

    # Create users
    admin = auth.register(
        "admin@shop.test", "admin", "Admin", "Root", "1 Rue du BO", is_admin=True
    )
    client = auth.register(
        "client@shop.test", "secret", "Alice", "Martin", "12 Rue des Fleurs"
    )

    token = auth.login("client@shop.test", "secret")
    user_id = sessions.get_user_id(token)

    print(
        "Produits:",
        [f"{p.name} {p.price_cents/100:.2f}€" for p in catalog.list_products()],
    )

    cart_svc.add_to_cart(user_id, p1.id, 2)
    cart_svc.add_to_cart(user_id, p2.id, 1)
    print("Total panier €:", cart_svc.cart_total(user_id) / 100)

    order = order_svc.checkout(user_id)
    print("Commande créée:", order.id, "Total €:", order.total_cents() / 100)

    order = order_svc.backoffice_validate_order(admin.id, order.id)
    print("Commande validée:", order.status)

    payment = order_svc.pay_by_card(order.id, "4242424242424242", 12, 2030, "123")
    print("Paiement OK:", payment.provider_ref)

    order = order_svc.backoffice_ship_order(admin.id, order.id)
    print("Expédiée, tracking:", order.delivery.tracking_number)
    order = order_svc.backoffice_mark_delivered(admin.id, order.id)
    print("Statut:", order.status)

    th = cs.open_thread(user_id, "Taille trop petite", order_id=order.id)
    cs.post_message(th.id, user_id, "Bonjour, je souhaite échanger le T-Shirt.")
    cs.post_message(
        th.id,
        None,
        "Bonjour, nous pouvons proposer un échange. Merci de renvoyer l'article.",
    )
    cs.close_thread(th.id, admin.id)
    print("Fil messages:", len(th.messages), "Fermé:", th.closed)

    auth.logout(token)
