"""Product repository for database operations"""
from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models_sql import ProductModel
import uuid


class ProductRepository:
    """Repository for product operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_product(
        self,
        name: str,
        description: Optional[str],
        image_url: Optional[str],
        price_cents: int,
        stock_qty: int,
        active: bool = True
    ) -> ProductModel:
        """Create a new product"""
        product = ProductModel(
            id=str(uuid.uuid4()),
            name=name,
            description=description,
            image_url=image_url,
            price_cents=price_cents,
            stock_qty=stock_qty,
            active=active
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product
    
    def get_product_by_id(self, product_id: str) -> Optional[ProductModel]:
        """Get a product by ID"""
        return self.db.query(ProductModel).filter(ProductModel.id == product_id).first()
    
    def get_all_products(self, active_only: bool = True) -> List[ProductModel]:
        """Get all products"""
        query = self.db.query(ProductModel)
        if active_only:
            query = query.filter(ProductModel.active == True)
        return query.all()
    
    def update_product(
        self,
        product_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        price_cents: Optional[int] = None,
        stock_qty: Optional[int] = None,
        active: Optional[bool] = None
    ) -> Optional[ProductModel]:
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
