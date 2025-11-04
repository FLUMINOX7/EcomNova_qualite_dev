"""Order-related Pydantic schemas"""
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


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
    validated_at: Optional[float] = None
    paid_at: Optional[float] = None
    shipped_at: Optional[float] = None
    delivered_at: Optional[float] = None
    cancelled_at: Optional[float] = None
    refunded_at: Optional[float] = None
    items: List[OrderItemResponse]
    total_price_cents: int
    invoice_id: Optional[str] = None
    payment_id: Optional[str] = None

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    """Schema for updating order status (admin only)"""
    status: OrderStatus
