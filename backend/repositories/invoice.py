"""Invoice repository for database operations"""

from __future__ import annotations

import time
import uuid

from sqlalchemy.orm import Session

from backend.models_sql import InvoiceLineModel, InvoiceModel


class InvoiceRepository:
    """Repository for invoice operations"""

    def __init__(self, db: Session):
        self.db = db

    def create_invoice(
        self, order_id: str, user_id: str, lines_data: list[dict], total_cents: int
    ) -> InvoiceModel:
        """Create a new invoice with lines"""
        invoice = InvoiceModel(
            id=str(uuid.uuid4()),
            order_id=order_id,
            user_id=user_id,
            total_cents=total_cents,
            issued_at=time.time(),
        )
        self.db.add(invoice)

        # Create invoice lines
        for line_data in lines_data:
            line = InvoiceLineModel(
                id=str(uuid.uuid4()),
                invoice_id=invoice.id,
                product_id=line_data["product_id"],
                name=line_data["name"],
                unit_price_cents=line_data["unit_price_cents"],
                quantity=line_data["quantity"],
                line_total_cents=line_data["unit_price_cents"] * line_data["quantity"],
            )
            self.db.add(line)

        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def get_by_id(self, invoice_id: str) -> InvoiceModel | None:
        """Get an invoice by ID"""
        return self.db.query(InvoiceModel).filter(InvoiceModel.id == invoice_id).first()

    def get_by_order(self, order_id: str) -> InvoiceModel | None:
        """Get invoice for an order"""
        return (
            self.db.query(InvoiceModel)
            .filter(InvoiceModel.order_id == order_id)
            .first()
        )

    def list_by_user(self, user_id: str) -> list[InvoiceModel]:
        """Get all invoices for a user"""
        return (
            self.db.query(InvoiceModel)
            .filter(InvoiceModel.user_id == user_id)
            .order_by(InvoiceModel.issued_at.desc())
            .all()
        )
