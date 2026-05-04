"""Runtime wiring for core domain (backend/core.py)
Creates in-memory singletons for repositories and services.
"""

from __future__ import annotations

from backend.core import (AuthService, BillingService, CartRepository,
                          CartService, CatalogService, DeliveryService,
                          InvoiceRepository, OrderRepository, OrderService,
                          PaymentGateway, PaymentRepository, ProductRepository,
                          SessionManager, UserRepository)

# Singletons (in-memory)
users = UserRepository()
products = ProductRepository()
carts = CartRepository()
orders = OrderRepository()
invoices = InvoiceRepository()
payments = PaymentRepository()
sessions = SessionManager()

# Services wired
auth_service = AuthService(users, sessions)
catalog_service = CatalogService(products)
cart_service = CartService(carts, products)
billing_service = BillingService(invoices)
delivery_service = DeliveryService()
payment_gateway = PaymentGateway()
order_service = OrderService(
    orders,
    products,
    carts,
    payments,
    invoices,
    billing_service,
    delivery_service,
    payment_gateway,
    users,
)


def core_services() -> tuple[
    AuthService,
    CatalogService,
    CartService,
    OrderService,
    SessionManager,
]:
    """Convenience accessor for endpoints."""
    return auth_service, catalog_service, cart_service, order_service, sessions
