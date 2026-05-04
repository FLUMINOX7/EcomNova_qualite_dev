"""Product-related Pydantic schemas"""

from __future__ import annotations

from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base schema for product"""

    name: str = Field(min_length=1)
    description: str | None = None
    image_url: str | None = None
    price_cents: int = Field(gt=0, description="Price in cents")
    stock_qty: int = Field(ge=0, description="Stock quantity")
    active: bool = True


class ProductCreate(ProductBase):
    """Schema for creating a product (admin only)"""

    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (admin only)"""

    name: str | None = Field(None, min_length=1)
    description: str | None = None
    image_url: str | None = None
    price_cents: int | None = Field(None, gt=0)
    stock_qty: int | None = Field(None, ge=0)
    active: bool | None = None


class ProductResponse(ProductBase):
    """Schema for product response"""

    id: str

    class Config:
        from_attributes = True
