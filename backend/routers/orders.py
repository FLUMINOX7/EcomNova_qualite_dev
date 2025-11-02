"""Order endpoints"""
from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.dependencies import get_session
from backend.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate, OrderItemResponse
from backend.repositories.order import OrderRepository
from backend.auth.jwt import get_current_user_id, require_admin
import backend.models_sql

router = APIRouter(prefix="/orders", tags=["Orders"])


def _build_order_response(order) -> OrderResponse:
    """Helper to build order response with item details"""
    items_response = []
    total_price = 0
    
    for item in order.items:
        item_total = item.unit_price_cents * item.quantity
        items_response.append(OrderItemResponse(
            id=item.id,
            product_id=item.product_id,
            name=item.name,
            unit_price_cents=item.unit_price_cents,
            quantity=item.quantity,
            total_price_cents=item_total
        ))
        total_price += item_total
    
    return OrderResponse(
        id=order.id,
        user_id=order.user_id,
        status=order.status,
        created_at=order.created_at,
        validated_at=order.validated_at,
        paid_at=order.paid_at,
        shipped_at=order.shipped_at,
        delivered_at=order.delivered_at,
        cancelled_at=order.cancelled_at,
        refunded_at=order.refunded_at,
        items=items_response,
        total_price_cents=total_price,
        invoice_id=order.invoice_id,
        payment_id=order.payment_id
    )


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Create a new order from cart"""
    repo = OrderRepository(db)
    order = repo.create_order_from_cart(user_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )
    
    return _build_order_response(order)


@router.get("", response_model=List[OrderResponse])
def list_orders(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """List current user's orders"""
    repo = OrderRepository(db)
    orders = repo.get_user_orders(user_id)
    return [_build_order_response(o) for o in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Get a specific order"""
    repo = OrderRepository(db)
    order = repo.get_order_by_id(order_id, user_id=user_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return _build_order_response(order)


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: str,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_session),
    admin_id: str = Depends(require_admin)
):
    """Update order status (admin only)"""
    repo = OrderRepository(db)
    order = repo.update_order_status(order_id, status_data.status)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return _build_order_response(order)


@router.get("/admin/all", response_model=List[OrderResponse])
def list_all_orders(
    db: Session = Depends(get_session),
    admin_id: str = Depends(require_admin)
):
    """List all orders (admin only)"""
    repo = OrderRepository(db)
    orders = repo.get_all_orders()
    return [_build_order_response(o) for o in orders]
