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
    const text = await res.text()
    throw new Error(`${res.status} ${res.statusText}: ${text}`)
  }
  
  try {
    return await res.json()
  } catch (e) {
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

// Auth (using /core endpoints for domain logic)
export function register(email, password, firstName, lastName, address) {
  return request('/core/register', {
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
  return request('/core/login', {
    method: 'POST',
    body: JSON.stringify({ email, password })
  })
}

// Cart (using /core endpoints)
export function fetchCart() {
  return request('/core/cart')
}

export function addToCartAPI(productId, quantity = 1) {
  return request('/core/cart/add', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity })
  })
}

export function removeFromCartAPI(productId, quantity = 1) {
  return request('/core/cart/remove', {
    method: 'POST',
    body: JSON.stringify({ product_id: productId, quantity })
  })
}

// Orders (using /core endpoints)
export function checkout() {
  return request('/core/checkout', {
    method: 'POST'
  })
}

export default {
  fetchProducts,
  fetchProduct,
  createProduct,
  register,
  login,
  fetchCart,
  addToCartAPI,
  removeFromCartAPI,
  checkout
}

