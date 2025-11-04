import React, { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { fetchProduct } from '../utils/api'
import { useCart } from '../contexts/CartContext'

export default function Product() {
  const { id } = useParams()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [quantity, setQuantity] = useState(1)
  const [message, setMessage] = useState('')
  
  const { addToCart } = useCart()
  const navigate = useNavigate()

  useEffect(() => {
    fetchProduct(id)
      .then(data => {
        setProduct(data)
        setLoading(false)
      })
      .catch(err => {
        console.error(err)
        setLoading(false)
      })
  }, [id])

  const handleAddToCart = () => {
    if (product) {
      addToCart(product, quantity)
      setMessage(`${quantity} article(s) ajouté(s) au panier !`)
      setTimeout(() => setMessage(''), 3000)
    }
  }

  if (loading) return <div className="loading">Chargement...</div>
  if (!product) return <div className="error">Produit introuvable</div>

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto' }}>
      <button 
        onClick={() => navigate('/')}
        className="btn btn-secondary"
        style={{ marginBottom: '2rem' }}
      >
        ← Retour au catalogue
      </button>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '3rem' }}>
        <div>
          <img
            src={product.image_url || product.image || '/assets/placeholder.svg'}
            alt={product.name}
            onError={(e) => {
              e.currentTarget.onerror = null
              e.currentTarget.src = '/assets/placeholder.svg'
            }}
            style={{
              width: '100%',
              borderRadius: '12px',
              border: '1px solid var(--border-glow)'
            }}
          />
        </div>

        <div>
          <h1 style={{ marginBottom: '1rem', fontSize: '2rem' }}>{product.name}</h1>
          <p className="price" style={{ fontSize: '2rem', marginBottom: '1.5rem' }}>
            {product.price_cents ? `${(product.price_cents / 100).toFixed(2)} €` : 'Prix non disponible'}
          </p>

          <p style={{ color: 'var(--text-secondary)', lineHeight: '1.7', marginBottom: '2rem' }}>
            {product.description || 'Aucune description disponible'}
          </p>

          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', marginBottom: '0.5rem' }}>Quantité</label>
            <input
              type="number"
              min="1"
              max={product.stock_qty || 99}
              value={quantity}
              onChange={(e) => setQuantity(parseInt(e.target.value) || 1)}
              style={{ width: '100px' }}
            />
            <span style={{ marginLeft: '1rem', color: 'var(--text-secondary)' }}>
              En stock: {product.stock_qty !== undefined ? product.stock_qty : 'N/A'}
            </span>
          </div>

          {message && <div className="success">{message}</div>}

          <button onClick={handleAddToCart} className="btn" style={{ width: '100%', fontSize: '1.1rem' }}>
            Ajouter au panier
          </button>
        </div>
      </div>
    </div>
  )
}

