"""Pytest configuration and shared fixtures for testing."""
import pytest
from fastapi.testclient import TestClient
from backend.app import app
from backend.core_runtime import (
    users, products, carts, orders, sessions,
    auth_service, catalog_service, cart_service, order_service
)


@pytest.fixture(scope="function")
def client():
    """Provide a FastAPI test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function", autouse=True)
def reset_core_state():
    """Reset in-memory core repositories before each test."""
    # Clear all in-memory data
    users._by_id.clear()
    users._by_email.clear()
    products._by_id.clear()
    carts._by_user.clear()
    orders._by_id.clear()
    orders._by_user.clear()
    sessions._sessions.clear()
    
    yield
    
    # Clean up after test
    users._by_id.clear()
    users._by_email.clear()
    products._by_id.clear()
    carts._by_user.clear()
    orders._by_id.clear()
    orders._by_user.clear()
    sessions._sessions.clear()


@pytest.fixture
def sample_product():
    """Create a sample product in the in-memory catalog."""
    from backend.core import Product
    import uuid
    product = Product(
        id=str(uuid.uuid4()),
        name="Test Product",
        description="A product for testing",
        price_cents=2500,
        stock_qty=50,
        active=True
    )
    products.add(product)
    return product


@pytest.fixture
def registered_user(client):
    """Register and return a test user with auth token."""
    user_data = {
        "email": "testuser@example.com",
        "password": "testpass123",
        "first_name": "Test",
        "last_name": "User",
        "address": "123 Test Street"
    }
    
    # Register
    response = client.post("/core/auth/register", json=user_data)
    assert response.status_code == 200
    user = response.json()
    
    # Login to get token
    login_response = client.post("/core/auth/login", json={
        "email": user_data["email"],
        "password": user_data["password"]
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    
    return {
        "user": user,
        "token": token,
        "credentials": user_data
    }
