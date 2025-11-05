"""Cart repository for database operations"""

from __future__ import annotations

import time
import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models_sql import (CartItemModel, CartModel, ProductModel,
                                UserModel)


class CartRepository:
    """Repository for cart operations"""

    def __init__(self, db: Session):
        self.db = db

    def get_or_create_cart(self, user_id: str) -> CartModel:
        """Get user's cart or create if doesn't exist"""
        # First verify the user exists
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found. Please log in again.",
                headers={"WWW-Authenticate": "Bearer"},
            )

        cart = self.db.query(CartModel).filter(CartModel.user_id == user_id).first()
        if not cart:
            cart = CartModel(user_id=user_id, created_at=time.time())
            self.db.add(cart)
            self.db.commit()
            self.db.refresh(cart)
        return cart

    def add_item(self, user_id: str, product_id: str, quantity: int) -> CartItemModel:
        """Add or update item in cart"""
        cart = self.get_or_create_cart(user_id)

        # Check if item already exists
        existing_item = (
            self.db.query(CartItemModel)
            .filter(
                CartItemModel.cart_user_id == user_id,
                CartItemModel.product_id == product_id,
            )
            .first()
        )

        # Verify product and stock
        product = (
            self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
        )
        if not product or not product.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is not available",
            )

        # Compute desired total quantity in cart for this product
        current_qty = existing_item.quantity if existing_item else 0
        desired_qty = current_qty + quantity
        if desired_qty <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be positive",
            )
        if desired_qty > product.stock_qty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Only {product.stock_qty} left",
            )

        if existing_item:
            existing_item.quantity = desired_qty
            self.db.commit()
            self.db.refresh(existing_item)
            return existing_item
        else:
            new_item = CartItemModel(
                id=str(uuid.uuid4()),
                cart_user_id=user_id,
                product_id=product_id,
                quantity=desired_qty,
            )
            self.db.add(new_item)
            self.db.commit()
            self.db.refresh(new_item)
            return new_item

    def update_item_quantity(
        self, item_id: str, quantity: int, user_id: str
    ) -> CartItemModel | None:
        """Update cart item quantity"""
        item = (
            self.db.query(CartItemModel)
            .filter(CartItemModel.id == item_id, CartItemModel.cart_user_id == user_id)
            .first()
        )

        if not item:
            return None

        if quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be positive",
            )

        # Verify stock against product
        product = (
            self.db.query(ProductModel)
            .filter(ProductModel.id == item.product_id)
            .first()
        )
        if not product or not product.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product is not available",
            )
        if quantity > product.stock_qty:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock. Only {product.stock_qty} left",
            )

        item.quantity = quantity
        self.db.commit()
        self.db.refresh(item)
        return item

    def remove_item(self, item_id: str, user_id: str) -> bool:
        """Remove item from cart"""
        item = (
            self.db.query(CartItemModel)
            .filter(CartItemModel.id == item_id, CartItemModel.cart_user_id == user_id)
            .first()
        )

        if not item:
            return False

        self.db.delete(item)
        self.db.commit()
        return True

    def get_cart_with_items(self, user_id: str) -> CartModel:
        """Get cart with all items and product details"""
        cart = self.get_or_create_cart(user_id)
        return cart

    def clear_cart(self, user_id: str) -> None:
        """Clear all items from cart"""
        self.db.query(CartItemModel).filter(
            CartItemModel.cart_user_id == user_id
        ).delete()
        self.db.commit()
