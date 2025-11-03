import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useCart } from '../contexts/CartContext'
import { useAuth } from '../contexts/AuthContext'

export default function Cart() {
  const { cart, updateQuantity, removeFromCart, getTotalPrice } = useCart()
  const { isAuthenticated } = useAuth()
  const navigate = useNavigate()

  if (cart.items.length === 0) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <h2>Votre panier est vide</h2>
        <p style={{ color: 'var(--text-secondary)', margin: '1rem 0 2rem 0' }}>
          Découvrez nos produits innovants !
        </p>
        <Link to="/" className="btn">
          Retour au catalogue
        </Link>
      </div>
    )
  }

  const handleCheckout = () => {
    if (!isAuthenticated) {
      navigate('/auth')
    } else {
      navigate('/checkout')
    }
  }

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '2rem' }}>Panier</h1>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem', marginBottom: '2rem' }}>
        {cart.items.map(item => (
          <div
            key={item.product.id}
            style={{
              background: 'var(--card-bg)',
              border: '1px solid var(--border-glow)',
              borderRadius: '12px',
              padding: '1.5rem',
              display: 'flex',
              gap: '1.5rem',
              alignItems: 'center'
            }}
          >
            <img
              src={item.product.image || '/assets/placeholder.svg'}
              alt={item.product.name}
              style={{
                width: '100px',
                height: '100px',
                objectFit: 'cover',
                borderRadius: '8px'
              }}
            />

            <div style={{ flex: 1 }}>
              <h3>{item.product.name}</h3>
              <p className="price">{item.product.price} €</p>
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <button
                onClick={() => updateQuantity(item.product.id, item.quantity - 1)}
                className="btn btn-secondary"
                style={{ width: '40px', padding: '0.5rem' }}
              >
                -
              </button>
              <span style={{ minWidth: '40px', textAlign: 'center', fontSize: '1.2rem' }}>
                {item.quantity}
              </span>
              <button
                onClick={() => updateQuantity(item.product.id, item.quantity + 1)}
                className="btn btn-secondary"
                style={{ width: '40px', padding: '0.5rem' }}
              >
                +
              </button>
            </div>

            <div style={{ textAlign: 'right', minWidth: '100px' }}>
              <div style={{ fontSize: '1.2rem', fontWeight: 'bold', color: 'var(--galaxy-cyan)' }}>
                {(item.product.price * item.quantity).toFixed(2)} €
              </div>
              <button
                onClick={() => removeFromCart(item.product.id)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#f87171',
                  cursor: 'pointer',
                  marginTop: '0.5rem',
                  textDecoration: 'underline'
                }}
              >
                Supprimer
              </button>
            </div>
          </div>
        ))}
      </div>

      <div
        style={{
          background: 'var(--card-bg)',
          border: '1px solid var(--border-glow)',
          borderRadius: '12px',
          padding: '2rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}
      >
        <div>
          <h2>Total</h2>
          <p style={{ color: 'var(--text-secondary)' }}>
            {cart.items.reduce((sum, item) => sum + item.quantity, 0)} article(s)
          </p>
        </div>
        <div style={{ textAlign: 'right' }}>
          <div style={{ fontSize: '2rem', fontWeight: 'bold', color: 'var(--galaxy-cyan)', marginBottom: '1rem' }}>
            {getTotalPrice().toFixed(2)} €
          </div>
          <button onClick={handleCheckout} className="btn" style={{ fontSize: '1.1rem', padding: '1rem 2rem' }}>
            {isAuthenticated ? 'Commander' : 'Se connecter pour commander'}
          </button>
        </div>
      </div>
    </div>
  )
}
