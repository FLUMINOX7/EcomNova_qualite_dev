"""Product-related Pydantic schemas"""
from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field


class ProductBase(BaseModel):
    """Base schema for product"""
    name: str = Field(min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = None
    price_cents: int = Field(gt=0, description="Price in cents")
    stock_qty: int = Field(ge=0, description="Stock quantity")
    active: bool = True


class ProductCreate(ProductBase):
    """Schema for creating a product (admin only)"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (admin only)"""
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = None
    image_url: Optional[str] = None
    price_cents: Optional[int] = Field(None, gt=0)
    stock_qty: Optional[int] = Field(None, ge=0)
    active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: str

    class Config:
        from_attributes = True
