import React, { createContext, useContext, useState, useEffect } from 'react'
import { useAuth } from './AuthContext'
import { useNotify } from './NotificationContext'
import { getCart as apiGetCart, addCartItem, updateCartItem, removeCartItem } from '../utils/api'

const CartContext = createContext(null)

export function CartProvider({ children }) {
  const [cart, setCart] = useState({ items: [] })
  const { isAuthenticated, logout } = useAuth()
  const { show } = useNotify()

  useEffect(() => {
    // Load cart from localStorage
    const savedCart = localStorage.getItem('cart')
    if (savedCart) {
      setCart(JSON.parse(savedCart))
    }
  }, [])

  useEffect(() => {
    // Save cart to localStorage whenever it changes
    localStorage.setItem('cart', JSON.stringify(cart))
  }, [cart])

  // Handle API errors (especially 401)
  const handleApiError = (error, operation = 'cart operation') => {
    if (error.isAuthError || error.status === 401) {
      show('Session expired. Please log in again.', 'error')
      logout()
      return true // Signal that this was an auth error
    }
    console.error(`Cart ${operation} failed:`, error)
    show(error.message || `Failed to ${operation}`, 'error')
    return false
  }

  // When user becomes authenticated, sync local cart to server, then load server cart
  useEffect(() => {
    const sync = async () => {
      if (!isAuthenticated) return
      try {
        // Push local items to server
        for (const item of cart.items) {
          await addCartItem(item.product.id, item.quantity)
        }
        // Fetch server cart and enrich with product details minimal mapping
        const serverCart = await apiGetCart()
        // Map server response items to our structure (no images available here)
        const items = serverCart.items.map(it => ({
          itemId: it.id,
          product: {
            id: it.product_id,
            name: it.product_name,
            price_cents: it.unit_price_cents,
            image_url: it.product_image_url,
          },
          quantity: it.quantity,
        }))
        setCart({ items })
      } catch (e) {
        handleApiError(e, 'sync')
      }
    }
    sync()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated])

  const addToCart = async (product, quantity = 1) => {
    // If authenticated, add to server first, then refresh from server
    if (isAuthenticated) {
      try {
        await addCartItem(product.id, quantity)
        const serverCart = await apiGetCart()
        const items = serverCart.items.map(it => ({
          itemId: it.id,
          product: { id: it.product_id, name: it.product_name, price_cents: it.unit_price_cents, image_url: it.product_image_url },
          quantity: it.quantity,
        }))
        setCart({ items })
      } catch (error) {
        handleApiError(error, 'add to cart')
        throw error
      }
      return
    }
    setCart(prev => {
      const existingItem = prev.items.find(item => item.product.id === product.id)
      
      if (existingItem) {
        return {
          ...prev,
          items: prev.items.map(item =>
            item.product.id === product.id
              ? { ...item, quantity: item.quantity + quantity }
              : item
          )
        }
      }
      
      return {
        ...prev,
        items: [...prev.items, { product, quantity }]
      }
    })
  }

  const updateQuantity = async (productId, quantity, itemId) => {
    if (quantity <= 0) {
      await removeFromCart(productId, itemId)
      return
    }
    if (isAuthenticated && itemId) {
      try {
        await updateCartItem(itemId, quantity)
        const serverCart = await apiGetCart()
        const items = serverCart.items.map(it => ({
          itemId: it.id,
          product: { id: it.product_id, name: it.product_name, price_cents: it.unit_price_cents, image_url: it.product_image_url },
          quantity: it.quantity,
        }))
        setCart({ items })
      } catch (error) {
        handleApiError(error, 'update quantity')
        throw error
      }
      return
    }
    setCart(prev => ({
      ...prev,
      items: prev.items.map(item =>
        item.product.id === productId
          ? { ...item, quantity }
          : item
      )
    }))
  }

  const removeFromCart = async (productId, itemId) => {
    if (isAuthenticated && itemId) {
      try {
        await removeCartItem(itemId)
        const serverCart = await apiGetCart()
        const items = serverCart.items.map(it => ({
          itemId: it.id,
          product: { id: it.product_id, name: it.product_name, price_cents: it.unit_price_cents },
          quantity: it.quantity,
        }))
        setCart({ items })
      } catch (error) {
        handleApiError(error, 'remove item')
        throw error
      }
      return
    }
    setCart(prev => ({
      ...prev,
      items: prev.items.filter(item => item.product.id !== productId)
    }))
  }

  const clearCart = () => {
    setCart({ items: [] })
  }

  const getTotalPrice = () => {
    return cart.items.reduce((total, item) => {
      const unit = item.product.price_cents ? item.product.price_cents / 100 : 0
      return total + unit * item.quantity
    }, 0)
  }

  const getTotalItems = () => {
    return cart.items.reduce((total, item) => total + item.quantity, 0)
  }

  const value = {
    cart,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    getTotalPrice,
    getTotalItems
  }

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>
}

export function useCart() {
  const context = useContext(CartContext)
  if (!context) {
    throw new Error('useCart must be used within CartProvider')
  }
  return context
}
