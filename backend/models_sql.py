from __future__ import annotations
from typing import List, Optional
import enum
from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    Text,
    Float,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from backend.db import Base


class OrderStatusEnum(str, enum.Enum):
    CREE = "CREE"
    VALIDEE = "VALIDEE"
    PAYEE = "PAYEE"
    EXPEDIEE = "EXPEDIEE"
    LIVREE = "LIVREE"
    ANNULEE = "ANNULEE"
    REMBOURSEE = "REMBOURSEE"


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=False)

    # relationships
    orders = relationship("OrderModel", back_populates="user", cascade="all, delete-orphan")
    cart = relationship("CartModel", uselist=False, back_populates="user", cascade="all, delete-orphan")


class ProductModel(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price_cents = Column(Integer, nullable=False)
    stock_qty = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)

    # relationships
    order_items = relationship("OrderItemModel", back_populates="product")
    cart_items = relationship("CartItemModel", back_populates="product")


class CartModel(Base):
    __tablename__ = "carts"
    # Use user_id as PK to have one cart per user
    user_id = Column(String, ForeignKey("users.id"), primary_key=True)
    created_at = Column(Float, nullable=False)

    user = relationship("UserModel", back_populates="cart")
    items = relationship("CartItemModel", back_populates="cart", cascade="all, delete-orphan")


class CartItemModel(Base):
    __tablename__ = "cart_items"
    id = Column(String, primary_key=True)
    cart_user_id = Column(String, ForeignKey("carts.user_id"), nullable=False, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    cart = relationship("CartModel", back_populates="items")
    product = relationship("ProductModel", back_populates="cart_items")


class OrderModel(Base):
    __tablename__ = "orders"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    status = Column(Enum(OrderStatusEnum), nullable=False, default=OrderStatusEnum.CREE)
    created_at = Column(Float, nullable=False)
    validated_at = Column(Float, nullable=True)
    paid_at = Column(Float, nullable=True)
    shipped_at = Column(Float, nullable=True)
    delivered_at = Column(Float, nullable=True)
    cancelled_at = Column(Float, nullable=True)
    refunded_at = Column(Float, nullable=True)
    invoice_id = Column(String, nullable=True)
    payment_id = Column(String, nullable=True)

    user = relationship("UserModel", back_populates="orders")
    items = relationship("OrderItemModel", back_populates="order", cascade="all, delete-orphan")


class OrderItemModel(Base):
    __tablename__ = "order_items"
    id = Column(String, primary_key=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    name = Column(String, nullable=False)
    unit_price_cents = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel", back_populates="order_items")
