-- Script de création des tables EcomNova
-- Généré depuis les modèles SQLAlchemy

-- Users table
CREATE TABLE users (
    id VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    password_hash VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    address TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT false,
    PRIMARY KEY (id)
);
CREATE INDEX ix_users_email ON users(email);
CREATE INDEX ix_users_id ON users(id);

-- Products table
CREATE TABLE products (
    id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    description TEXT,
    price_cents INTEGER NOT NULL,
    stock_qty INTEGER NOT NULL,
    active BOOLEAN DEFAULT true,
    PRIMARY KEY (id)
);
CREATE INDEX ix_products_id ON products(id);

-- Carts table (one per user)
CREATE TABLE carts (
    user_id VARCHAR NOT NULL,
    created_at FLOAT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Cart items
CREATE TABLE cart_items (
    id VARCHAR NOT NULL,
    cart_user_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(cart_user_id) REFERENCES carts (user_id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES products (id)
);
CREATE INDEX ix_cart_items_cart_user_id ON cart_items(cart_user_id);

-- Orders table
CREATE TABLE orders (
    id VARCHAR NOT NULL,
    user_id VARCHAR NOT NULL,
    status VARCHAR NOT NULL,  -- enum: CREE, VALIDEE, PAYEE, EXPEDIEE, LIVREE, ANNULEE, REMBOURSEE
    created_at FLOAT NOT NULL,
    validated_at FLOAT,
    paid_at FLOAT,
    shipped_at FLOAT,
    delivered_at FLOAT,
    cancelled_at FLOAT,
    refunded_at FLOAT,
    invoice_id VARCHAR,
    payment_id VARCHAR,
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES users (id)
);
CREATE INDEX ix_orders_user_id ON orders(user_id);

-- Order items
CREATE TABLE order_items (
    id VARCHAR NOT NULL,
    order_id VARCHAR NOT NULL,
    product_id VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    unit_price_cents INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY(order_id) REFERENCES orders (id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES products (id)
);
CREATE INDEX ix_order_items_order_id ON order_items(order_id);

-- Note: Pour exécuter ce script
-- psql -U ecomnova_user -d ecomnova -a -f backend/schema.sql