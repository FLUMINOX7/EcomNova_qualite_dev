import time
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db import Base
from backend.models_sql import (CartItemModel, CartModel, OrderItemModel,
                                OrderModel, OrderStatusEnum, ProductModel,
                                UserModel)


def test_models_sql_basic():
    """Create tables in an in-memory SQLite DB and perform basic CRUD to validate models."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create a user
    user = UserModel(
        id=str(uuid.uuid4()),
        email="u@test.local",
        password_hash="hash",
        first_name="Jean",
        last_name="Dupont",
        address="1 rue test",
        is_admin=False,
    )
    session.add(user)

    # Create products
    p1 = ProductModel(
        id=str(uuid.uuid4()),
        name="Prod1",
        description="d",
        price_cents=1000,
        stock_qty=10,
    )
    p2 = ProductModel(
        id=str(uuid.uuid4()),
        name="Prod2",
        description="d2",
        price_cents=2500,
        stock_qty=5,
    )
    session.add_all([p1, p2])

    # Create cart for user and add cart items
    cart = CartModel(user_id=user.id, created_at=time.time())
    ci = CartItemModel(
        id=str(uuid.uuid4()), cart_user_id=user.id, product_id=p1.id, quantity=2
    )
    cart.items.append(ci)
    session.add(cart)

    # Create an order from cart
    order = OrderModel(
        id=str(uuid.uuid4()),
        user_id=user.id,
        created_at=time.time(),
        status=OrderStatusEnum.CREE,
    )
    oi = OrderItemModel(
        id=str(uuid.uuid4()),
        order_id=order.id,
        product_id=p1.id,
        name=p1.name,
        unit_price_cents=p1.price_cents,
        quantity=2,
    )
    order.items.append(oi)
    session.add(order)

    session.commit()

    # Queries
    u = session.query(UserModel).filter_by(email="u@test.local").one_or_none()
    assert u is not None and u.email == "u@test.local"

    prod = session.query(ProductModel).filter_by(name="Prod1").one_or_none()
    assert prod is not None and prod.price_cents == 1000

    got_cart = session.query(CartModel).filter_by(user_id=user.id).one_or_none()
    assert got_cart is not None and len(got_cart.items) == 1

    got_order = session.query(OrderModel).filter_by(user_id=user.id).one_or_none()
    assert (
        got_order is not None
        and len(got_order.items) == 1
        and got_order.items[0].unit_price_cents == 1000
    )

    session.close()


if __name__ == "__main__":
    test_models_sql_basic()
    print("models-sql smoke: OK")
