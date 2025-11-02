"""Order repository for database operations"""
from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models_sql import OrderModel, OrderItemModel, CartItemModel, ProductModel, OrderStatusEnum
import uuid
import time


class OrderRepository:
    """Repository for order operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_order_from_cart(self, user_id: str) -> Optional[OrderModel]:
        """Create an order from user's cart"""
        # Get cart items
        cart_items = self.db.query(CartItemModel).filter(
            CartItemModel.cart_user_id == user_id
        ).all()
        
        if not cart_items:
            return None  # Empty cart
        
        # Create order
        order = OrderModel(
            id=str(uuid.uuid4()),
            user_id=user_id,
            status=OrderStatusEnum.CREE,
            created_at=time.time()
        )
        self.db.add(order)
        
        # Create order items from cart
        for cart_item in cart_items:
            product = self.db.query(ProductModel).filter(
                ProductModel.id == cart_item.product_id
            ).first()
            
            if not product:
                continue
            
            order_item = OrderItemModel(
                id=str(uuid.uuid4()),
                order_id=order.id,
                product_id=product.id,
                name=product.name,
                unit_price_cents=product.price_cents,
                quantity=cart_item.quantity
            )
            self.db.add(order_item)
        
        # Clear cart
        for cart_item in cart_items:
            self.db.delete(cart_item)
        
        self.db.commit()
        self.db.refresh(order)
        return order
    
    def get_order_by_id(self, order_id: str, user_id: Optional[str] = None) -> Optional[OrderModel]:
        """Get an order by ID"""
        query = self.db.query(OrderModel).filter(OrderModel.id == order_id)
        if user_id:
            query = query.filter(OrderModel.user_id == user_id)
        return query.first()
    
    def get_user_orders(self, user_id: str) -> List[OrderModel]:
        """Get all orders for a user"""
        return self.db.query(OrderModel).filter(
            OrderModel.user_id == user_id
        ).order_by(OrderModel.created_at.desc()).all()
    
    def get_all_orders(self) -> List[OrderModel]:
        """Get all orders (admin only)"""
        return self.db.query(OrderModel).order_by(OrderModel.created_at.desc()).all()
    
    def update_order_status(
        self,
        order_id: str,
        status: OrderStatusEnum
    ) -> Optional[OrderModel]:
        """Update order status"""
        order = self.get_order_by_id(order_id)
        if not order:
            return None
        
        order.status = status
        
        # Update timestamps based on status
        now = time.time()
        if status == OrderStatusEnum.VALIDEE and not order.validated_at:
            order.validated_at = now
        elif status == OrderStatusEnum.PAYEE and not order.paid_at:
            order.paid_at = now
        elif status == OrderStatusEnum.EXPEDIEE and not order.shipped_at:
            order.shipped_at = now
        elif status == OrderStatusEnum.LIVREE and not order.delivered_at:
            order.delivered_at = now
        elif status == OrderStatusEnum.ANNULEE and not order.cancelled_at:
            order.cancelled_at = now
        elif status == OrderStatusEnum.REMBOURSEE and not order.refunded_at:
            order.refunded_at = now
        
        self.db.commit()
        self.db.refresh(order)
        return order
