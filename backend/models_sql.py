from __future__ import annotations
from sqlalchemy import Column, String, Integer, Boolean, Text
from sqlalchemy.orm import relationship
from .db import Base


class UserModel(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(Text, nullable=False)
    is_admin = Column(Boolean, default=False)


class ProductModel(Base):
    __tablename__ = "products"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price_cents = Column(Integer, nullable=False)
    stock_qty = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
