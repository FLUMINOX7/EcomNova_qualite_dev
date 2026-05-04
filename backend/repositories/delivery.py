"""Delivery repository for database operations"""

from __future__ import annotations

import time
import uuid

from sqlalchemy.orm import Session

from backend.models_sql import DeliveryModel


class DeliveryRepository:
    """Repository for delivery operations"""

    def __init__(self, db: Session):
        self.db = db

    def create_delivery(
        self,
        order_id: str,
        carrier: str,
        tracking_number: str,
        address: str,
        status: str = "PREPAREE",
    ) -> DeliveryModel:
        """Create a new delivery record"""
        delivery = DeliveryModel(
            id=str(uuid.uuid4()),
            order_id=order_id,
            carrier=carrier,
            tracking_number=tracking_number,
            address=address,
            status=status,
            created_at=time.time(),
        )
        self.db.add(delivery)
        self.db.commit()
        self.db.refresh(delivery)
        return delivery

    def get_by_id(self, delivery_id: str) -> DeliveryModel | None:
        """Get a delivery by ID"""
        return (
            self.db.query(DeliveryModel).filter(DeliveryModel.id == delivery_id).first()
        )

    def get_by_order(self, order_id: str) -> DeliveryModel | None:
        """Get delivery for an order"""
        return (
            self.db.query(DeliveryModel)
            .filter(DeliveryModel.order_id == order_id)
            .first()
        )

    def update_status(self, delivery_id: str, status: str) -> DeliveryModel | None:
        """Update delivery status"""
        delivery = self.get_by_id(delivery_id)
        if delivery:
            delivery.status = status
            self.db.commit()
            self.db.refresh(delivery)
        return delivery

    def update_tracking(
        self, delivery_id: str, tracking_number: str
    ) -> DeliveryModel | None:
        """Update tracking number"""
        delivery = self.get_by_id(delivery_id)
        if delivery:
            delivery.tracking_number = tracking_number
            self.db.commit()
            self.db.refresh(delivery)
        return delivery
