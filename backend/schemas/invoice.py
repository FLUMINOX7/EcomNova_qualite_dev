"""Pydantic schemas for invoices"""

from pydantic import BaseModel


class InvoiceLineResponse(BaseModel):
    """Invoice line response"""

    id: str
    product_id: str
    name: str
    unit_price_cents: int
    quantity: int
    line_total_cents: int

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    """Invoice response"""

    id: str
    order_id: str
    user_id: str
    total_cents: int
    issued_at: float
    lines: list[InvoiceLineResponse]

    class Config:
        from_attributes = True
