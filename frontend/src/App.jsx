import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { CartProvider, useCart } from './contexts/CartContext'
import Catalog from './pages/Catalog'
import Product from './pages/Product'
import Cart from './pages/Cart'
import Auth from './pages/Auth'
import Checkout from './pages/Checkout'

function AppContent() {
  const { isAuthenticated, user, logout } = useAuth()
  const { getTotalItems } = useCart()

  return (
    <div className="app-root">
      <header className="site-header">
        <Link to="/" className="logo">EcomNova</Link>
        <nav>
          <Link to="/cart">
            Panier {getTotalItems() > 0 && `(${getTotalItems()})`}
          </Link>
          {isAuthenticated ? (
            <>
              <span style={{ color: 'var(--galaxy-cyan)' }}>
                {user?.email}
              </span>
              <button onClick={logout} className="btn btn-secondary">
                Déconnexion
              </button>
            </>
          ) : (
            <Link to="/auth">Connexion</Link>
          )}
        </nav>
      </header>

      <main className="site-main">
        <Routes>
          <Route path="/" element={<Catalog />} />
          <Route path="/product/:id" element={<Product />} />
          <Route path="/cart" element={<Cart />} />
          <Route path="/checkout" element={<Checkout />} />
          <Route path="/auth" element={<Auth />} />
        </Routes>
      </main>

      <footer className="site-footer">
        © 2025 EcomNova - Cutting-edge technology for tomorrow
      </footer>
    </div>
  )
}

export default function App() {
  return (
    <AuthProvider>
      <CartProvider>
        <AppContent />
      </CartProvider>
    </AuthProvider>
  )
}
