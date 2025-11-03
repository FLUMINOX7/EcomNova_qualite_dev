import React, { createContext, useContext, useState, useEffect } from 'react'
import { useAuth } from './AuthContext'
import { getCart as apiGetCart, addCartItem, updateCartItem, removeCartItem } from '../utils/api'

const CartContext = createContext(null)

export function CartProvider({ children }) {
  const [cart, setCart] = useState({ items: [] })
  const { isAuthenticated } = useAuth()

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
          },
          quantity: it.quantity,
        }))
        setCart({ items })
      } catch (e) {
        // silent fail keeps local cart
        console.error('Cart sync failed', e)
      }
    }
    sync()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [isAuthenticated])

  const addToCart = async (product, quantity = 1) => {
    // If authenticated, add to server first, then refresh from server
    if (isAuthenticated) {
      await addCartItem(product.id, quantity)
      const serverCart = await apiGetCart()
      const items = serverCart.items.map(it => ({
        itemId: it.id,
        product: { id: it.product_id, name: it.product_name, price_cents: it.unit_price_cents },
        quantity: it.quantity,
      }))
      setCart({ items })
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
      await updateCartItem(itemId, quantity)
      const serverCart = await apiGetCart()
      const items = serverCart.items.map(it => ({
        itemId: it.id,
        product: { id: it.product_id, name: it.product_name, price_cents: it.unit_price_cents },
        quantity: it.quantity,
      }))
      setCart({ items })
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
      await removeCartItem(itemId)
      const serverCart = await apiGetCart()
      const items = serverCart.items.map(it => ({
        itemId: it.id,
        product: { id: it.product_id, name: it.product_name, price_cents: it.unit_price_cents },
        quantity: it.quantity,
      }))
      setCart({ items })
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
