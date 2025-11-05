"""Product repository for database operations"""

from __future__ import annotations

import uuid

from sqlalchemy.orm import Session

from backend.models_sql import ProductModel


class ProductRepository:
    """Repository for product operations"""

    def __init__(self, db: Session):
        self.db = db

    def create_product(
        self,
        name: str,
        description: str | None,
        image_url: str | None,
        price_cents: int,
        stock_qty: int,
        active: bool = True,
    ) -> ProductModel:
        """Create a new product"""
        product = ProductModel(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            image_url=image_url,
            price_cents=price_cents,
            stock_qty=stock_qty,
            active=active,
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_product_by_id(self, product_id: str) -> ProductModel | None:
        """Get a product by ID"""
        return self.db.query(ProductModel).filter(ProductModel.id == product_id).first()

    def get_all_products(self, active_only: bool = True) -> list[ProductModel]:
        """Get all products"""
        query = self.db.query(ProductModel)
        if active_only:
            query = query.filter(ProductModel.active == True)
        return query.all()

    def update_product(
        self,
        product_id: str,
        name: str | None = None,
        description: str | None = None,
        image_url: str | None = None,
        price_cents: int | None = None,
        stock_qty: int | None = None,
        active: bool | None = None,
    ) -> ProductModel | None:
        """Update a product"""
        product = self.get_product_by_id(product_id)
        if not product:
            return None

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if image_url is not None:
            product.image_url = image_url
        if price_cents is not None:
            product.price_cents = price_cents
        if stock_qty is not None:
            product.stock_qty = stock_qty
        if active is not None:
            product.active = active

        self.db.commit()
        self.db.refresh(product)
        return product

    def decrease_stock(self, product_id: str, quantity: int) -> bool:
        """Decrease product stock (for orders)"""
        product = self.get_product_by_id(product_id)
        if not product or product.stock_qty < quantity:
            return False

        product.stock_qty -= quantity
        self.db.commit()
        return True

    def increase_stock(self, product_id: str, quantity: int) -> bool:
        """Increase product stock (for cancellations/refunds)"""
        product = self.get_product_by_id(product_id)
        if not product:
            return False

        product.stock_qty += quantity
        self.db.commit()
        return True
