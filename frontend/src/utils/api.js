const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request(path, opts = {}) {
  const url = `${API_BASE}${path}`
  const res = await fetch(url, opts)
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

export function fetchProducts() {
  return request('/products')
}

export default { fetchProducts }
