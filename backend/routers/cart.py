"""Cart endpoints"""
from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.dependencies import get_session
from backend.schemas.cart import CartResponse, CartItemAdd, CartItemUpdate, CartItemResponse
from backend.repositories.cart import CartRepository
from backend.repositories.product import ProductRepository
from backend.auth.jwt import get_current_user_id
from backend.models_sql import ProductModel

router = APIRouter(prefix="/cart", tags=["Cart"])


def _build_cart_response(cart, db: Session) -> CartResponse:
    """Helper to build cart response with item details"""
    items_response = []
    total_price = 0
    total_items = 0
    
    for item in cart.items:
        product = db.query(ProductModel).filter(
            ProductModel.id == item.product_id
        ).first()
        
        if product:
            item_total = product.price_cents * item.quantity
            items_response.append(CartItemResponse(
                id=item.id,
                product_id=product.id,
                product_name=product.name,
                product_image_url=product.image_url,
                unit_price_cents=product.price_cents,
                quantity=item.quantity,
                total_price_cents=item_total
            ))
            total_price += item_total
            total_items += item.quantity
    
    return CartResponse(
        user_id=cart.user_id,
        items=items_response,
        total_price_cents=total_price,
        total_items=total_items
    )


@router.get("", response_model=CartResponse)
def get_cart(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Get current user's cart"""
    repo = CartRepository(db)
    cart = repo.get_cart_with_items(user_id)
    return _build_cart_response(cart, db)


@router.post("/items", response_model=CartResponse, status_code=status.HTTP_201_CREATED)
def add_cart_item(
    item_data: CartItemAdd,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Add item to cart"""
    # Verify product exists
    product_repo = ProductRepository(db)
    product = product_repo.get_product_by_id(item_data.product_id)
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if not product.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is not available"
        )
    
    if product.stock_qty < item_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient stock"
        )
    
    # Add to cart
    cart_repo = CartRepository(db)
    cart_repo.add_item(user_id, item_data.product_id, item_data.quantity)
    
    # Return updated cart
    cart = cart_repo.get_cart_with_items(user_id)
    return _build_cart_response(cart, db)


@router.put("/items/{item_id}", response_model=CartResponse)
def update_cart_item(
    item_id: str,
    item_data: CartItemUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Update cart item quantity"""
    repo = CartRepository(db)
    item = repo.update_item_quantity(item_id, item_data.quantity, user_id)
    
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    # Return updated cart
    cart = repo.get_cart_with_items(user_id)
    return _build_cart_response(cart, db)


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_cart_item(
    item_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_session)
):
    """Remove item from cart"""
    repo = CartRepository(db)
    success = repo.remove_item(item_id, user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    
    return None
