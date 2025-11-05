"""Cart-related Pydantic schemas"""

from __future__ import annotations

from pydantic import BaseModel, Field


class CartItemAdd(BaseModel):
    """Schema for adding item to cart"""

    product_id: str
    quantity: int = Field(gt=0, description="Quantity must be positive")


class CartItemUpdate(BaseModel):
    """Schema for updating cart item quantity"""

    quantity: int = Field(gt=0, description="Quantity must be positive")


class CartItemResponse(BaseModel):
    """Schema for cart item response"""

    id: str
    product_id: str
    product_name: str
    product_image_url: str | None = None
    unit_price_cents: int
    product_stock_qty: int
    quantity: int
    total_price_cents: int

    class Config:
        from_attributes = True


class CartResponse(BaseModel):
    """Schema for cart response"""

    user_id: str
    items: list[CartItemResponse]
    total_price_cents: int
    total_items: int

    class Config:
        from_attributes = True
