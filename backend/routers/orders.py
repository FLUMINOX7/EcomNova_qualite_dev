"""Order endpoints"""

from __future__ import annotations

import time
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.jwt import get_current_user_id, require_admin
from backend.dependencies import get_session
from backend.models_sql import OrderStatusEnum, UserModel
from backend.repositories.delivery import DeliveryRepository
from backend.repositories.invoice import InvoiceRepository
from backend.repositories.order import OrderRepository
from backend.repositories.payment import PaymentRepository
from backend.repositories.product import ProductRepository
from backend.schemas.delivery import DeliveryResponse
from backend.schemas.order import (OrderCreate, OrderItemResponse,
                                   OrderResponse, OrderStatusUpdate)
from backend.schemas.payment import PaymentCardData, PaymentResponse
from backend.services.payment import PaymentService

router = APIRouter(prefix="/orders", tags=["Orders"])


def _build_order_response(order) -> OrderResponse:
    """Helper to build order response with item details"""
    items_response = []
    total_price = 0

    for item in order.items:
        item_total = item.unit_price_cents * item.quantity
        items_response.append(
            OrderItemResponse(
                id=item.id,
                product_id=item.product_id,
                name=item.name,
                unit_price_cents=item.unit_price_cents,
                quantity=item.quantity,
                total_price_cents=item_total,
            )
        )
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
        payment_id=order.payment_id,
    )


@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session),
):
    """Create a new order from cart"""
    repo = OrderRepository(db)
    order = repo.create_order_from_cart(user_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty"
        )

    return _build_order_response(order)


@router.get("", response_model=list[OrderResponse])
def list_orders(
    user_id: str = Depends(get_current_user_id), db: Session = Depends(get_session)
):
    """List current user's orders"""
    repo = OrderRepository(db)
    orders = repo.get_user_orders(user_id)
    return [_build_order_response(o) for o in orders]


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session),
):
    """Get a specific order"""
    repo = OrderRepository(db)
    order = repo.get_order_by_id(order_id, user_id=user_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return _build_order_response(order)


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: str,
    status_data: OrderStatusUpdate,
    db: Session = Depends(get_session),
    admin_id: str = Depends(require_admin),
):
    """Update order status (admin only)"""
    repo = OrderRepository(db)
    order = repo.update_order_status(order_id, status_data.status)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return _build_order_response(order)


@router.get("/admin/all", response_model=list[OrderResponse])
def list_all_orders(
    db: Session = Depends(get_session), admin_id: str = Depends(require_admin)
):
    """List all orders (admin only)"""
    repo = OrderRepository(db)
    orders = repo.get_all_orders()
    return [_build_order_response(o) for o in orders]


@router.post(
    "/{order_id}/pay",
    response_model=PaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def pay_order(
    order_id: str,
    card_data: PaymentCardData,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session),
):
    """Pay for an order with a credit card (simulation)"""
    order_repo = OrderRepository(db)
    payment_repo = PaymentRepository(db)
    invoice_repo = InvoiceRepository(db)

    # Get order and verify ownership
    order = order_repo.get_order_by_id(order_id, user_id=user_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check order status
    if order.status not in [OrderStatusEnum.CREE, OrderStatusEnum.VALIDEE]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot pay order with status {order.status}",
        )

    # Calculate total
    total_cents = sum(item.unit_price_cents * item.quantity for item in order.items)

    # Process payment via gateway
    payment_service = PaymentService()
    result = payment_service.process_payment(
        order_id=order_id,
        card_number=card_data.card_number,
        exp_month=card_data.exp_month,
        exp_year=card_data.exp_year,
        cvc=card_data.cvc,
        amount_cents=total_cents,
    )

    # Create payment record
    payment = payment_repo.create_payment(
        order_id=order_id,
        user_id=user_id,
        amount_cents=total_cents,
        provider="CB",
        provider_ref=result.get("transaction_id"),
        succeeded=result["success"],
    )

    if not payment.succeeded:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=result.get("failure_reason", "Payment failed"),
        )

    # Update order
    order.payment_id = payment.id
    order.status = OrderStatusEnum.PAYEE
    order.paid_at = time.time()

    # Generate invoice
    lines_data = [
        {
            "product_id": item.product_id,
            "name": item.name,
            "unit_price_cents": item.unit_price_cents,
            "quantity": item.quantity,
        }
        for item in order.items
    ]
    invoice = invoice_repo.create_invoice(
        order_id=order_id,
        user_id=user_id,
        lines_data=lines_data,
        total_cents=total_cents,
    )
    order.invoice_id = invoice.id

    db.commit()
    db.refresh(payment)

    return payment


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session),
):
    """Cancel an order (before shipment) and restore stock"""
    order_repo = OrderRepository(db)
    product_repo = ProductRepository(db)

    # Get order and verify ownership
    order = order_repo.get_order_by_id(order_id, user_id=user_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check if order can be cancelled
    if order.status in [OrderStatusEnum.EXPEDIEE, OrderStatusEnum.LIVREE]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot cancel order that has been shipped",
        )

    if order.status in [OrderStatusEnum.ANNULEE, OrderStatusEnum.REMBOURSEE]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order already cancelled or refunded",
        )

    # Restore stock
    for item in order.items:
        product_repo.increase_stock(item.product_id, item.quantity)

    # Update order status
    order.status = OrderStatusEnum.ANNULEE
    order.cancelled_at = time.time()

    db.commit()
    db.refresh(order)

    return _build_order_response(order)


@router.post(
    "/{order_id}/ship",
    response_model=DeliveryResponse,
    status_code=status.HTTP_201_CREATED,
)
def ship_order(
    order_id: str,
    admin_id: str = Depends(require_admin),
    db: Session = Depends(get_session),
):
    """Ship an order (admin only) - generates tracking number and creates delivery"""
    order_repo = OrderRepository(db)
    delivery_repo = DeliveryRepository(db)

    # Get order
    order = order_repo.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check order status
    if order.status != OrderStatusEnum.PAYEE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot ship order with status {order.status}. Order must be PAYEE.",
        )

    # Get user address
    user = db.query(UserModel).filter(UserModel.id == order.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Generate tracking number
    tracking_number = f"TRK-{uuid.uuid4().hex[:10].upper()}"

    # Create delivery
    delivery = delivery_repo.create_delivery(
        order_id=order_id,
        carrier="POSTE",
        tracking_number=tracking_number,
        address=user.address,
        status="EN_COURS",
    )

    # Update order
    order.status = OrderStatusEnum.EXPEDIEE
    order.shipped_at = time.time()

    db.commit()
    db.refresh(delivery)

    return delivery


@router.post("/{order_id}/deliver", response_model=OrderResponse)
def mark_delivered(
    order_id: str,
    admin_id: str = Depends(require_admin),
    db: Session = Depends(get_session),
):
    """Mark an order as delivered (admin only)"""
    order_repo = OrderRepository(db)
    delivery_repo = DeliveryRepository(db)

    # Get order
    order = order_repo.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check order status
    if order.status != OrderStatusEnum.EXPEDIEE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must be shipped before marking as delivered",
        )

    # Update delivery status
    delivery = delivery_repo.get_by_order(order_id)
    if delivery:
        delivery_repo.update_status(delivery.id, "LIVREE")

    # Update order
    order.status = OrderStatusEnum.LIVREE
    order.delivered_at = time.time()

    db.commit()
    db.refresh(order)

    return _build_order_response(order)


@router.post("/{order_id}/refund", response_model=OrderResponse)
def refund_order(
    order_id: str,
    admin_id: str = Depends(require_admin),
    db: Session = Depends(get_session),
):
    """Refund an order (admin only) - restores stock and processes refund"""
    order_repo = OrderRepository(db)
    payment_repo = PaymentRepository(db)
    product_repo = ProductRepository(db)

    # Get order
    order = order_repo.get_order_by_id(order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    # Check order status
    if order.status not in [
        OrderStatusEnum.PAYEE,
        OrderStatusEnum.ANNULEE,
        OrderStatusEnum.EXPEDIEE,
        OrderStatusEnum.LIVREE,
    ]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order cannot be refunded in current status",
        )

    if order.status == OrderStatusEnum.REMBOURSEE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Order already refunded"
        )

    # Get payment
    payment = payment_repo.get_by_order(order_id)
    if not payment or not payment.succeeded:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No successful payment found for this order",
        )

    # Process refund via gateway
    payment_service = PaymentService()
    total_cents = sum(item.unit_price_cents * item.quantity for item in order.items)
    refund_result = payment_service.process_refund(
        transaction_id=payment.provider_ref, amount_cents=total_cents
    )

    if not refund_result["success"]:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Refund processing failed",
        )

    # Restore stock
    for item in order.items:
        product_repo.increase_stock(item.product_id, item.quantity)

    # Update order
    order.status = OrderStatusEnum.REMBOURSEE
    order.refunded_at = time.time()

    db.commit()
    db.refresh(order)

    return _build_order_response(order)
