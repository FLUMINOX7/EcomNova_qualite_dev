"""Endpoints that expose the core domain (backend/core.py) in-memory services.
This integrates the given core.py into the FastAPI backend under a /core namespace.
"""
from __future__ import annotations
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, EmailStr, Field
from backend.core_runtime import core_services
from backend.core import Product

router = APIRouter(prefix="/core", tags=["Core (in-memory)"])


# ------------- Schemas (light wrappers) -------------
class CoreRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)
    first_name: str
    last_name: str
    address: str


class CoreLogin(BaseModel):
    email: EmailStr
    password: str


class CoreUser(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    address: str
    is_admin: bool


class CoreProductCreate(BaseModel):
    name: str
    description: str = ""
    price_cents: int = Field(gt=0)
    stock_qty: int = Field(ge=0)


class CoreProduct(BaseModel):
    id: str
    name: str
    description: str
    price_cents: int
    stock_qty: int
    active: bool


class CoreCartItem(BaseModel):
    product_id: str
    quantity: int


class CoreCart(BaseModel):
    user_id: str
    items: List[CoreCartItem]
    total_cents: int


class CoreOrder(BaseModel):
    id: str
    user_id: str
    total_cents: int
    status: str


# ------------- Helper -------------

def _require_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    return authorization.split(" ", 1)[1]


# ------------- Auth -------------
@router.post("/auth/register", response_model=CoreUser)
def core_register(payload: CoreRegister):
    auth, *_ = core_services()
    u = auth.register(
        email=payload.email,
        password=payload.password,
        first_name=payload.first_name,
        last_name=payload.last_name,
        address=payload.address,
    )
    return CoreUser(
        id=u.id,
        email=u.email,
        first_name=u.first_name,
        last_name=u.last_name,
        address=u.address,
        is_admin=u.is_admin,
    )


@router.post("/auth/login")
def core_login(payload: CoreLogin):
    auth, *_ = core_services()
    token = auth.login(payload.email, payload.password)
    return {"access_token": token, "token_type": "bearer"}


@router.get("/auth/me", response_model=CoreUser)
def core_me(authorization: Optional[str] = Header(default=None)):
    auth, _, _, _, sessions = core_services()
    token = _require_token(authorization)
    user_id = sessions.get_user_id(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    u = auth.users.get(user_id)
    return CoreUser(
        id=u.id,
        email=u.email,
        first_name=u.first_name,
        last_name=u.last_name,
        address=u.address,
        is_admin=u.is_admin,
    )


# ------------- Products -------------
@router.get("/products", response_model=List[CoreProduct])
def core_products_list():
    _, catalog, *_ = core_services()
    prods = catalog.list_products()
    return [CoreProduct(**p.__dict__) for p in prods]


@router.post("/products", response_model=CoreProduct)
def core_products_create(payload: CoreProductCreate):
    # For demo, allow anyone to create products in-memory
    from uuid import uuid4
    _, catalog, *_ = core_services()
    p = Product(
        id=str(uuid4()),
        name=payload.name,
        description=payload.description,
        price_cents=payload.price_cents,
        stock_qty=payload.stock_qty,
    )
    catalog.products.add(p)
    return CoreProduct(**p.__dict__)


# ------------- Cart -------------
class CoreCartAdd(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)


@router.get("/cart", response_model=CoreCart)
def core_cart(authorization: Optional[str] = Header(default=None)):
    _, catalog, cart, _, sessions = core_services()
    token = _require_token(authorization)
    user_id = sessions.get_user_id(token)
    c = cart.view_cart(user_id)
    items = [CoreCartItem(product_id=i.product_id, quantity=i.quantity) for i in c.items.values()]
    total = cart.cart_total(user_id)
    return CoreCart(user_id=user_id, items=items, total_cents=total)


@router.post("/cart/items", response_model=CoreCart)
def core_cart_add(payload: CoreCartAdd, authorization: Optional[str] = Header(default=None)):
    _, catalog, cart, _, sessions = core_services()
    token = _require_token(authorization)
    user_id = sessions.get_user_id(token)
    cart.add_to_cart(user_id, payload.product_id, payload.quantity)
    c = cart.view_cart(user_id)
    items = [CoreCartItem(product_id=i.product_id, quantity=i.quantity) for i in c.items.values()]
    total = cart.cart_total(user_id)
    return CoreCart(user_id=user_id, items=items, total_cents=total)


# ------------- Orders -------------
@router.post("/orders", response_model=CoreOrder)
def core_checkout(authorization: Optional[str] = Header(default=None)):
    *_, orders, sessions = core_services()
    token = _require_token(authorization)
    user_id = sessions.get_user_id(token)
    o = orders.checkout(user_id)
    return CoreOrder(id=o.id, user_id=o.user_id, total_cents=o.total_cents(), status=o.status.name)
