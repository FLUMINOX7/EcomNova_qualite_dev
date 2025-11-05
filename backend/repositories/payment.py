"""Payment repository for database operations"""

from __future__ import annotations

import time
import uuid

from sqlalchemy.orm import Session

from backend.models_sql import PaymentModel


class PaymentRepository:
    """Repository for payment operations"""

    def __init__(self, db: Session):
        self.db = db

    def create_payment(
        self,
        order_id: str,
        user_id: str,
        amount_cents: int,
        provider: str,
        provider_ref: str | None,
        succeeded: bool,
    ) -> PaymentModel:
        """Create a new payment record"""
        payment = PaymentModel(
            id=str(uuid.uuid4()),
            order_id=order_id,
            user_id=user_id,
            amount_cents=amount_cents,
            provider=provider,
            provider_ref=provider_ref,
            succeeded=succeeded,
            created_at=time.time(),
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def get_by_id(self, payment_id: str) -> PaymentModel | None:
        """Get a payment by ID"""
        return self.db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()

    def get_by_order(self, order_id: str) -> PaymentModel | None:
        """Get payment for an order"""
        return (
            self.db.query(PaymentModel)
            .filter(PaymentModel.order_id == order_id)
            .first()
        )

    def list_by_user(self, user_id: str) -> list[PaymentModel]:
        """Get all payments for a user"""
        return (
            self.db.query(PaymentModel)
            .filter(PaymentModel.user_id == user_id)
            .order_by(PaymentModel.created_at.desc())
            .all()
        )
