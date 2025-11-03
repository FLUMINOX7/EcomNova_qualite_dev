"""Integration tests for /core endpoints (in-memory domain)."""
import pytest


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


class TestCoreAuth:
    """Tests for /core/auth endpoints."""
    
    def test_register_new_user(self, client):
        """Test user registration."""
        user_data = {
            "email": "newuser@test.com",
            "password": "secure123",
            "first_name": "New",
            "last_name": "User",
            "address": "456 New St"
        }
        
        response = client.post("/core/auth/register", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["email"] == user_data["email"]
        assert data["first_name"] == user_data["first_name"]
        assert data["last_name"] == user_data["last_name"]
        assert data["is_admin"] is False
        assert "id" in data
        assert "password" not in data  # Password should not be returned
    
    def test_register_duplicate_email(self, client, registered_user):
        """Test registration with duplicate email fails."""
        user_data = {
            "email": registered_user["credentials"]["email"],
            "password": "different123",
            "first_name": "Another",
            "last_name": "Person",
            "address": "789 Duplicate Ave"
        }
        
        response = client.post("/core/auth/register", json=user_data)
        assert response.status_code == 400  # Bad Request
        assert "email" in response.json()["detail"].lower() or "utilisé" in response.json()["detail"].lower()
    
    def test_login_success(self, client, registered_user):
        """Test successful login."""
        login_data = {
            "email": registered_user["credentials"]["email"],
            "password": registered_user["credentials"]["password"]
        }
        
        response = client.post("/core/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
    
    def test_login_wrong_password(self, client, registered_user):
        """Test login with wrong password."""
        login_data = {
            "email": registered_user["credentials"]["email"],
            "password": "wrongpassword"
        }
        
        response = client.post("/core/auth/login", json=login_data)
        assert response.status_code == 401  # Unauthorized
    
    def test_login_nonexistent_user(self, client):
        """Test login with non-existent email."""
        login_data = {
            "email": "nobody@test.com",
            "password": "anypassword"
        }
        
        response = client.post("/core/auth/login", json=login_data)
        assert response.status_code == 401  # Unauthorized
    
    def test_get_current_user(self, client, registered_user):
        """Test getting current user info with valid token."""
        headers = {"Authorization": f"Bearer {registered_user['token']}"}
        
        response = client.get("/core/auth/me", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == registered_user["user"]["id"]
        assert data["email"] == registered_user["user"]["email"]
    
    def test_get_current_user_no_token(self, client):
        """Test /core/auth/me without token."""
        response = client.get("/core/auth/me")
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self, client):
        """Test /core/auth/me with invalid token."""
        headers = {"Authorization": "Bearer invalid-token-xyz"}
        
        response = client.get("/core/auth/me", headers=headers)
        assert response.status_code == 401


class TestCoreProducts:
    """Tests for /core/products endpoints."""
    
    def test_list_products_empty(self, client):
        """Test listing products when catalog is empty."""
        response = client.get("/core/products")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_list_products_with_items(self, client, sample_product):
        """Test listing products with items in catalog."""
        response = client.get("/core/products")
        assert response.status_code == 200
        
        products = response.json()
        assert len(products) == 1
        assert products[0]["id"] == sample_product.id
        assert products[0]["name"] == sample_product.name
        assert products[0]["price_cents"] == sample_product.price_cents
    
    def test_create_product(self, client):
        """Test creating a new product."""
        product_data = {
            "name": "New Product",
            "description": "Brand new item",
            "price_cents": 1500,
            "stock_qty": 100
        }
        
        response = client.post("/core/products", json=product_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["name"] == product_data["name"]
        assert data["description"] == product_data["description"]
        assert data["price_cents"] == product_data["price_cents"]
        assert data["stock_qty"] == product_data["stock_qty"]
        assert data["active"] is True
        assert "id" in data


class TestCoreCart:
    """Tests for /core/cart endpoints."""
    
    def test_view_empty_cart(self, client, registered_user):
        """Test viewing empty cart."""
        headers = {"Authorization": f"Bearer {registered_user['token']}"}
        
        response = client.get("/core/cart", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["user_id"] == registered_user["user"]["id"]
        assert data["items"] == []
        assert data["total_cents"] == 0
    
    def test_add_item_to_cart(self, client, registered_user, sample_product):
        """Test adding an item to cart."""
        headers = {"Authorization": f"Bearer {registered_user['token']}"}
        cart_item = {
            "product_id": sample_product.id,
            "quantity": 3
        }
        
        response = client.post("/core/cart/items", json=cart_item, headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == sample_product.id
        assert data["items"][0]["quantity"] == 3
        assert data["total_cents"] == sample_product.price_cents * 3
    
    def test_add_multiple_items(self, client, registered_user, sample_product):
        """Test adding same item multiple times increments quantity."""
        headers = {"Authorization": f"Bearer {registered_user['token']}"}
        cart_item = {
            "product_id": sample_product.id,
            "quantity": 2
        }
        
        # Add twice
        client.post("/core/cart/items", json=cart_item, headers=headers)
        response = client.post("/core/cart/items", json=cart_item, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["items"][0]["quantity"] == 4  # 2 + 2
        assert data["total_cents"] == sample_product.price_cents * 4
    
    def test_cart_requires_auth(self, client):
        """Test cart endpoints require authentication."""
        response = client.get("/core/cart")
        assert response.status_code == 401


class TestCoreOrders:
    """Tests for /core/orders endpoints."""
    
    def test_checkout_with_items(self, client, registered_user, sample_product):
        """Test creating order from cart."""
        headers = {"Authorization": f"Bearer {registered_user['token']}"}
        
        # Add item to cart
        cart_item = {"product_id": sample_product.id, "quantity": 2}
        client.post("/core/cart/items", json=cart_item, headers=headers)
        
        # Checkout
        response = client.post("/core/orders", headers=headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert data["user_id"] == registered_user["user"]["id"]
        assert data["total_cents"] == sample_product.price_cents * 2
        assert data["status"] == "CREE"
    
    def test_checkout_empty_cart(self, client, registered_user):
        """Test checkout with empty cart fails."""
        headers = {"Authorization": f"Bearer {registered_user['token']}"}
        
        response = client.post("/core/orders", headers=headers)
        assert response.status_code == 400  # Bad Request
        assert "panier" in response.json()["detail"].lower() or "vide" in response.json()["detail"].lower()
    
    def test_checkout_clears_cart(self, client, registered_user, sample_product):
        """Test that checkout clears the cart."""
        headers = {"Authorization": f"Bearer {registered_user['token']}"}
        
        # Add item and checkout
        cart_item = {"product_id": sample_product.id, "quantity": 1}
        client.post("/core/cart/items", json=cart_item, headers=headers)
        client.post("/core/orders", headers=headers)
        
        # Check cart is empty
        cart_response = client.get("/core/cart", headers=headers)
        assert cart_response.json()["items"] == []
        assert cart_response.json()["total_cents"] == 0


class TestCompleteFlow:
    """End-to-end test of complete user flow."""
    
    def test_full_ecommerce_flow(self, client):
        """Test complete flow: register → login → add products → cart → checkout."""
        # 1. Register
        user_data = {
            "email": "flow@test.com",
            "password": "test123",
            "first_name": "Flow",
            "last_name": "Test",
            "address": "123 Flow St"
        }
        reg_response = client.post("/core/auth/register", json=user_data)
        assert reg_response.status_code == 200
        
        # 2. Login
        login_response = client.post("/core/auth/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        # 3. Create product
        product_data = {
            "name": "Flow Product",
            "description": "For testing flow",
            "price_cents": 5000,
            "stock_qty": 10
        }
        product_response = client.post("/core/products", json=product_data)
        assert product_response.status_code == 200
        product_id = product_response.json()["id"]
        
        # 4. View products
        products_response = client.get("/core/products")
        assert len(products_response.json()) >= 1
        
        # 5. Add to cart
        cart_item = {"product_id": product_id, "quantity": 2}
        cart_response = client.post("/core/cart/items", json=cart_item, headers=headers)
        assert cart_response.status_code == 200
        assert cart_response.json()["total_cents"] == 10000  # 5000 * 2
        
        # 6. View cart
        view_cart_response = client.get("/core/cart", headers=headers)
        assert len(view_cart_response.json()["items"]) == 1
        
        # 7. Checkout
        order_response = client.post("/core/orders", headers=headers)
        assert order_response.status_code == 200
        assert order_response.json()["status"] == "CREE"
        assert order_response.json()["total_cents"] == 10000
        
        # 8. Verify cart is empty after checkout
        final_cart = client.get("/core/cart", headers=headers)
        assert final_cart.json()["items"] == []
