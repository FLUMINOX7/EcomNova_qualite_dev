import React from 'react'
import { Routes, Route, Link } from 'react-router-dom'
import { AuthProvider, useAuth } from './contexts/AuthContext'
import { CartProvider, useCart } from './contexts/CartContext'
import { NotificationProvider } from './contexts/NotificationContext'
import Catalog from './pages/Catalog'
import Product from './pages/Product'
import Cart from './pages/Cart'
import Auth from './pages/Auth'
import Checkout from './pages/Checkout'
import Profile from './pages/Profile'
import Orders from './pages/Orders'
import AdminDashboard from './pages/AdminDashboard'
import Support from './pages/Support'

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
              <Link to="/orders">Commandes</Link>
              <Link to="/support">Support</Link>
              {user?.is_admin && (
                <Link to="/admin" style={{ color: 'var(--galaxy-purple)' }}>
                  🛡️ Admin
                </Link>
              )}
              <Link to="/profile">Profil</Link>
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
          <Route path="/profile" element={<Profile />} />
          <Route path="/orders" element={<Orders />} />
          <Route path="/support" element={<Support />} />
          <Route path="/admin" element={<AdminDashboard />} />
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
    <NotificationProvider>
      <AuthProvider>
        <CartProvider>
          <AppContent />
        </CartProvider>
      </AuthProvider>
    </NotificationProvider>
  )
}
