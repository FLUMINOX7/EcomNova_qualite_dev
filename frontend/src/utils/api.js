const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, opts = {}) {
  const url = `${API_BASE}${path}`
  const token = localStorage.getItem('token')
  
  const headers = {
    'Content-Type': 'application/json',
    ...opts.headers
  }
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`
  }
  
  const res = await fetch(url, {
    ...opts,
    headers
  })
  
  if (!res.ok) {
    // Handle 401 Unauthorized - token expired or user deleted
    if (res.status === 401) {
      // Clear auth data
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      
      // Create a custom error that components can detect
      const error = new Error('Session expired. Please log in again.')
      error.status = 401
      error.isAuthError = true
      throw error
    }
    
    const text = await res.text()
    const error = new Error(`${res.status} ${res.statusText}: ${text}`)
    error.status = res.status
    throw error
  }
  
  try {
    return await res.json()
  } catch {
    return null
  }
}

// Products
export function fetchProducts() {
  return request('/products')
}

export function fetchProduct(id) {
  return request(`/products/${id}`)
}

export function createProduct(data) {
  return request('/products', {
    method: 'POST',
    body: JSON.stringify(data)
  })
}

// Auth (using SQL endpoints)
export function register(email, password, firstName, lastName, address) {
  return request('/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
      first_name: firstName,
      last_name: lastName,
      address
    })
  })
}

export function login(email, password) {
  return request('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  })
}

export function getMe() {
  return request('/auth/me')
}

export function updateMe(data) {
  return request('/auth/me', {
    method: 'PUT',
    body: JSON.stringify({
      email: data.email,
      first_name: data.first_name,
      last_name: data.last_name,
      address: data.address,
    })
  })
}

// Cart (using SQL endpoints)
export function getCart() {
  return request('/cart')
}

export function addCartItem(productId, quantity = 1) {
  return request('/cart/items', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity })
  })
}

export function updateCartItem(itemId, quantity) {
  return request(`/cart/items/${itemId}`, {
    method: 'PUT',
    body: JSON.stringify({ quantity })
  })
}

export function removeCartItem(itemId) {
  return request(`/cart/items/${itemId}`, {
    method: 'DELETE'
  })
}

// Orders (using SQL endpoints)
export function createOrder() {
  return request('/orders', {
    method: 'POST'
  })
}

export default {
  fetchProducts,
  fetchProduct,
  createProduct,
  register,
  login,
  getMe,
  updateMe,
  getCart,
  addCartItem,
  updateCartItem,
  removeCartItem,
  createOrder
}

