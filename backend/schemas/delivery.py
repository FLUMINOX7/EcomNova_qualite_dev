"""Pydantic schemas for delivery"""
from pydantic import BaseModel
from typing import Optional


class DeliveryResponse(BaseModel):
    """Delivery information response"""
    id: str
    order_id: str
    carrier: str
    tracking_number: Optional[str]
    address: str
    status: str  # PREPAREE, EN_COURS, LIVREE

    class Config:
        from_attributes = True


class DeliveryCreate(BaseModel):
    """Data for creating a delivery"""
    carrier: str = "POSTE"
    address: str
