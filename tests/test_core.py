import time

from backend import core


def test_full_order_flow():
    # Repos & services
    users = core.UserRepository()
    products = core.ProductRepository()
    carts = core.CartRepository()
    orders = core.OrderRepository()
    invoices = core.InvoiceRepository()
    payments = core.PaymentRepository()
    threads = core.ThreadRepository()
    sessions = core.SessionManager()

    auth = core.AuthService(users, sessions)
    catalog = core.CatalogService(products)
    cart_svc = core.CartService(carts, products)
    billing = core.BillingService(invoices)
    delivery_svc = core.DeliveryService()
    gateway = core.PaymentGateway()
    order_svc = core.OrderService(
        orders,
        products,
        carts,
        payments,
        invoices,
        billing,
        delivery_svc,
        gateway,
        users,
    )
    cs = core.CustomerService(threads, users)

    # Create products
    p1 = core.Product(
        id="p1", name="Item1", description="desc", price_cents=1000, stock_qty=5
    )
    products.add(p1)

    # Register users
    admin = auth.register("adm@test", "pwd", "A", "Admin", "addr", is_admin=True)
    client = auth.register("u@test", "pwd2", "U", "Client", "addr")

    # Login client
    token = auth.login("u@test", "pwd2")
    user_id = sessions.get_user_id(token)
    assert user_id == client.id

    # Add to cart and check total
    cart_svc.add_to_cart(user_id, "p1", 2)
    assert cart_svc.cart_total(user_id) == 2000

    # Checkout
    order = order_svc.checkout(user_id)
    assert order.total_cents() == 2000
    assert order.status == core.OrderStatus.CREE

    # Validate by admin
    order = order_svc.backoffice_validate_order(admin.id, order.id)
    assert order.status == core.OrderStatus.VALIDEE

    # Pay
    payment = order_svc.pay_by_card(order.id, "4242424242424242", 12, 2030, "123")
    assert payment.succeeded
    assert order.payment_id is not None

    # Ship
    order = order_svc.backoffice_ship_order(admin.id, order.id)
    assert order.status == core.OrderStatus.EXPEDIEE
    assert order.delivery is not None

    # Mark delivered
    order = order_svc.backoffice_mark_delivered(admin.id, order.id)
    assert order.status == core.OrderStatus.LIVREE

    # Open thread and post message
    th = cs.open_thread(user_id, "Help", order_id=order.id)
    msg = cs.post_message(th.id, user_id, "Bonjour")
    assert len(th.messages) == 1
