"""Pydantic schemas for payments"""

from pydantic import BaseModel, Field


class PaymentCardData(BaseModel):
    """Card payment information"""

    card_number: str = Field(
        ..., min_length=13, max_length=19, description="Card number (13-19 digits)"
    )
    exp_month: int = Field(..., ge=1, le=12, description="Expiration month (1-12)")
    exp_year: int = Field(..., ge=2025, description="Expiration year")
    cvc: str = Field(..., min_length=3, max_length=4, description="Card security code")


class PaymentResponse(BaseModel):
    """Payment response"""

    id: str
    order_id: str
    user_id: str
    amount_cents: int
    provider: str
    provider_ref: str | None
    succeeded: bool
    created_at: float

    class Config:
        from_attributes = True
