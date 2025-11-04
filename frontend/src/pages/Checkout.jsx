import React, { useMemo, useState } from 'react'
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
  // Payment simulation state
  const [cardName, setCardName] = useState('')
  const [cardNumber, setCardNumber] = useState('')
  const [expiry, setExpiry] = useState('') // MM/YY
  const [cvv, setCvv] = useState('')

  const digitsOnly = (s) => (s || '').replace(/\D/g, '')

  // Luhn algorithm for card number
  const isValidCardNumber = (num) => {
    const digits = digitsOnly(num)
    if (digits.length < 12) return false
    let sum = 0
    let shouldDouble = false
    for (let i = digits.length - 1; i >= 0; i--) {
      let d = parseInt(digits[i], 10)
      if (shouldDouble) {
        d *= 2
        if (d > 9) d -= 9
      }
      sum += d
      shouldDouble = !shouldDouble
    }
    return sum % 10 === 0
  }

  const isValidExpiry = (val) => {
    // Expect MM/YY
    const match = /^(0[1-9]|1[0-2])\/(\d{2})$/.exec(val)
    if (!match) return false
    const mm = parseInt(match[1], 10)
    const yy = parseInt(match[2], 10)
    const now = new Date()
    const currentYY = now.getFullYear() % 100
    const currentMM = now.getMonth() + 1
    // Expired if year < current or same year but month < current
    if (yy < currentYY) return false
    if (yy === currentYY && mm < currentMM) return false
    return true
  }

  const isValidCvv = (val) => /^\d{3,4}$/.test(val)

  const cardNumberDisplay = useMemo(() => {
    // Format as #### #### #### ####
    const d = digitsOnly(cardNumber).slice(0, 19)
    return d.replace(/(\d{4})(?=\d)/g, '$1 ').trim()
  }, [cardNumber])

  const canSubmit =
    cardName.trim().length >= 2 &&
    isValidCardNumber(cardNumber) &&
    isValidExpiry(expiry) &&
    isValidCvv(cvv) &&
    !loading

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
      // 1. Create order from cart
      const order = await createOrder()
      
      // 2. Pay the order with card details
      const token = localStorage.getItem('token')
      const [expMonth, expYear] = expiry.split('/')
      
      const paymentRes = await fetch(`${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/orders/${order.id}/pay`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          card_number: digitsOnly(cardNumber),
          exp_month: parseInt(expMonth, 10),
          exp_year: parseInt('20' + expYear, 10),
          cvc: cvv
        })
      })
      
      if (!paymentRes.ok) {
        const error = await paymentRes.json()
        throw new Error(error.detail || 'Paiement refusé')
      }
      
      setSuccess(true)
      clearCart()
      show('Commande payée avec succès !', 'success')
      
      setTimeout(() => {
        navigate('/orders')
      }, 3000)
    } catch (err) {
      show(err.message || 'Erreur lors du paiement', 'error')
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

        {/* Right column - Payment + Delivery info (simulation) */}
        <div>
          <h2 style={{ marginBottom: '1rem' }}>Paiement (simulation)</h2>
          
          <div style={{ 
            background: 'var(--card-bg)', 
            border: '1px solid var(--border-glow)', 
            borderRadius: '12px', 
            padding: '1.5rem' 
          }}>
            <p style={{ 
              background: 'rgba(56,189,248,0.08)',
              border: '1px solid var(--border-glow)',
              borderRadius: '8px',
              padding: '0.75rem 1rem',
              marginBottom: '1rem',
              color: 'var(--text-secondary)'
            }}>
              Cette section simule un paiement CB. Aucune donnée de carte n’est envoyée au serveur.
            </p>

            <div style={{ display: 'grid', gap: '1rem' }}>
              <div>
                <label htmlFor="cardName" style={{ display: 'block', marginBottom: '.35rem' }}>Nom sur la carte</label>
                <input
                  id="cardName"
                  type="text"
                  value={cardName}
                  onChange={(e) => setCardName(e.target.value)}
                  placeholder="Jean Dupont"
                  style={{ width: '100%' }}
                />
              </div>

              <div>
                <label htmlFor="cardNumber" style={{ display: 'block', marginBottom: '.35rem' }}>Numéro de carte</label>
                <input
                  id="cardNumber"
                  type="text"
                  inputMode="numeric"
                  autoComplete="cc-number"
                  value={cardNumberDisplay}
                  onChange={(e) => setCardNumber(e.target.value)}
                  placeholder="4242 4242 4242 4242"
                  aria-invalid={cardNumber && !isValidCardNumber(cardNumber) ? 'true' : 'false'}
                  style={{ width: '100%' }}
                />
                {cardNumber && !isValidCardNumber(cardNumber) && (
                  <div role="alert" style={{ color: '#f87171', fontSize: '.9rem', marginTop: '.25rem' }}>
                    Numéro de carte invalide
                  </div>
                )}
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
                <div>
                  <label htmlFor="expiry" style={{ display: 'block', marginBottom: '.35rem' }}>Expiration (MM/AA)</label>
                  <input
                    id="expiry"
                    type="text"
                    inputMode="numeric"
                    autoComplete="cc-exp"
                    value={expiry}
                    onChange={(e) => setExpiry(e.target.value.replace(/[^0-9/]/g, '').slice(0, 5))}
                    placeholder="12/27"
                    aria-invalid={expiry && !isValidExpiry(expiry) ? 'true' : 'false'}
                    style={{ width: '100%' }}
                  />
                  {expiry && !isValidExpiry(expiry) && (
                    <div role="alert" style={{ color: '#f87171', fontSize: '.9rem', marginTop: '.25rem' }}>
                      Date d’expiration invalide
                    </div>
                  )}
                </div>

                <div>
                  <label htmlFor="cvv" style={{ display: 'block', marginBottom: '.35rem' }}>CVV</label>
                  <input
                    id="cvv"
                    type="password"
                    inputMode="numeric"
                    autoComplete="cc-csc"
                    value={cvv}
                    onChange={(e) => setCvv(e.target.value.replace(/\D/g, '').slice(0, 4))}
                    placeholder="123"
                    aria-invalid={cvv && !isValidCvv(cvv) ? 'true' : 'false'}
                    style={{ width: '100%' }}
                  />
                  {cvv && !isValidCvv(cvv) && (
                    <div role="alert" style={{ color: '#f87171', fontSize: '.9rem', marginTop: '.25rem' }}>
                      CVV invalide (3 ou 4 chiffres)
                    </div>
                  )}
                </div>
              </div>

              <hr style={{ border: 'none', borderTop: '1px solid var(--border-glow)' }} />

              <h3 style={{ margin: '0.5rem 0 0.25rem 0' }}>Informations de livraison</h3>
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
              disabled={!canSubmit}
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
              Simulation de paiement — aucune donnée n’est transmise
            </p>
            {/* End grid wrapper */}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
