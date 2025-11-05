"""Product endpoints"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.auth.jwt import require_admin
from backend.dependencies import get_session
from backend.repositories.product import ProductRepository
from backend.schemas.product import (ProductCreate, ProductResponse,
                                     ProductUpdate)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_session)):
    """List all active products"""
    repo = ProductRepository(db)
    products = repo.get_all_products(active_only=True)
    return [ProductResponse.from_orm(p) for p in products]


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: str, db: Session = Depends(get_session)):
    """Get a specific product by ID"""
    repo = ProductRepository(db)
    product = repo.get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return ProductResponse.from_orm(product)


@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_session),
    admin_id: str = Depends(require_admin),
):
    """Create a new product (admin only)"""
    repo = ProductRepository(db)
    product = repo.create_product(
        name=product_data.name,
        description=product_data.description,
        image_url=product_data.image_url,
        price_cents=product_data.price_cents,
        stock_qty=product_data.stock_qty,
        active=product_data.active,
    )
    return ProductResponse.from_orm(product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: str,
    product_data: ProductUpdate,
    db: Session = Depends(get_session),
    admin_id: str = Depends(require_admin),
):
    """Update a product (admin only)"""
    repo = ProductRepository(db)
    product = repo.update_product(
        product_id=product_id,
        name=product_data.name,
        description=product_data.description,
        image_url=product_data.image_url,
        price_cents=product_data.price_cents,
        stock_qty=product_data.stock_qty,
        active=product_data.active,
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return ProductResponse.from_orm(product)
