"""Order-related Pydantic schemas"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class OrderStatus(str, Enum):
    """Order status enum"""

    CREE = "CREE"
    VALIDEE = "VALIDEE"
    PAYEE = "PAYEE"
    EXPEDIEE = "EXPEDIEE"
    LIVREE = "LIVREE"
    ANNULEE = "ANNULEE"
    REMBOURSEE = "REMBOURSEE"


class OrderItemResponse(BaseModel):
    """Schema for order item response"""

    id: str
    product_id: str
    name: str
    unit_price_cents: int
    quantity: int
    total_price_cents: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    """Schema for creating an order from cart"""

    pass  # Orders are created from the user's cart


class OrderResponse(BaseModel):
    """Schema for order response"""

    id: str
    user_id: str
    status: OrderStatus
    created_at: float
    validated_at: float | None = None
    paid_at: float | None = None
    shipped_at: float | None = None
    delivered_at: float | None = None
    cancelled_at: float | None = None
    refunded_at: float | None = None
    items: list[OrderItemResponse]
    total_price_cents: int
    invoice_id: str | None = None
    payment_id: str | None = None

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status (admin only)"""

    status: OrderStatus
