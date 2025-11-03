import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useCart } from '../contexts/CartContext'
import { useAuth } from '../contexts/AuthContext'
import { useNotify } from '../contexts/NotificationContext'
import { createOrder } from '../utils/api'

export default function Checkout() {
  const { cart, clearCart, getTotalPrice } = useCart()
  const { user, isAuthenticated } = useAuth()
  const { show } = useNotify()
  const navigate = useNavigate()
  
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  if (!isAuthenticated) {
    navigate('/auth')
    return null
  }

  if (cart.items.length === 0) {
    navigate('/cart')
    return null
  }

  const handleOrder = async () => {
    setLoading(true)

    try {
      await createOrder()
      setSuccess(true)
      clearCart()
      show('Commande confirmée avec succès !', 'success')
      
      setTimeout(() => {
        navigate('/')
      }, 3000)
    } catch (err) {
      show(err.message || 'Erreur lors de la commande', 'error')
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div style={{ textAlign: 'center', padding: '3rem' }}>
        <div className="success" style={{ maxWidth: '600px', margin: '0 auto 2rem auto' }}>
          <h2>✓ Commande confirmée !</h2>
          <p>Votre commande a été enregistrée avec succès.</p>
          <p>Vous allez être redirigé vers l'accueil...</p>
        </div>
      </div>
    )
  }

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '2rem' }}>Finaliser la commande</h1>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        {/* Left column - Order summary */}
        <div>
          <h2 style={{ marginBottom: '1rem' }}>Récapitulatif</h2>
          
          <div style={{ 
            background: 'var(--card-bg)', 
            border: '1px solid var(--border-glow)', 
            borderRadius: '12px', 
            padding: '1.5rem' 
          }}>
            {cart.items.map(item => (
              <div 
                key={item.product.id}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  marginBottom: '1rem',
                  paddingBottom: '1rem',
                  borderBottom: '1px solid var(--border-glow)'
                }}
              >
                <div>
                  <div style={{ fontWeight: '600' }}>{item.product.name}</div>
                  <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
                    Quantité: {item.quantity}
                  </div>
                </div>
                <div style={{ fontWeight: '600', color: 'var(--galaxy-cyan)' }}>
                  {((item.product.price_cents / 100) * item.quantity).toFixed(2)} €
                </div>
              </div>
            ))}

            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              marginTop: '1.5rem',
              paddingTop: '1rem',
              borderTop: '2px solid var(--galaxy-bright)',
              fontSize: '1.3rem',
              fontWeight: 'bold'
            }}>
              <span>Total</span>
              <span style={{ color: 'var(--galaxy-cyan)' }}>
                {getTotalPrice().toFixed(2)} €
              </span>
            </div>
          </div>
        </div>

        {/* Right column - Delivery info */}
        <div>
          <h2 style={{ marginBottom: '1rem' }}>Informations de livraison</h2>
          
          <div style={{ 
            background: 'var(--card-bg)', 
            border: '1px solid var(--border-glow)', 
            borderRadius: '12px', 
            padding: '1.5rem' 
          }}>
            <div style={{ marginBottom: '1rem' }}>
              <strong>Email:</strong>
              <div style={{ color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                {user?.email}
              </div>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <strong>Nom:</strong>
              <div style={{ color: 'var(--text-secondary)', marginTop: '0.25rem' }}>
                {user?.first_name} {user?.last_name}
              </div>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <strong>Adresse de livraison:</strong>
              <div style={{ color: 'var(--text-secondary)', marginTop: '0.25rem', whiteSpace: 'pre-line' }}>
                {user?.address}
              </div>
            </div>

            <button 
              onClick={handleOrder}
              disabled={loading}
              className="btn"
              style={{ width: '100%', fontSize: '1.1rem', padding: '1rem' }}
            >
              {loading ? 'Traitement en cours...' : 'Confirmer et payer'}
            </button>

            <p style={{ 
              fontSize: '0.85rem', 
              color: 'var(--text-secondary)', 
              textAlign: 'center', 
              marginTop: '1rem' 
            }}>
              Paiement sécurisé via EcomNova
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
