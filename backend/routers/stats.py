"""Statistics endpoints"""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.dependencies import get_session
from backend.models_sql import OrderModel, ProductModel, UserModel

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("")
def get_statistics(db: Session = Depends(get_session)):
    """Get general statistics for the homepage"""

    # Count products
    products_count = (
        db.query(func.count(ProductModel.id))
        .filter(ProductModel.active == True)
        .scalar()
        or 0
    )

    # Count users (excluding admin accounts)
    users_count = (
        db.query(func.count(UserModel.id)).filter(UserModel.is_admin == False).scalar()
        or 0
    )

    # Count total orders
    orders_count = db.query(func.count(OrderModel.id)).scalar() or 0

    # Calculate satisfaction (mock percentage based on orders)
    satisfaction = 98 if orders_count > 0 else 100

    return {
        "products": products_count,
        "customers": max(users_count, 1200 + users_count * 10),  # Boost for demo
        "orders": max(orders_count, 850 + orders_count * 15),  # Boost for demo
        "satisfaction": satisfaction,
    }
