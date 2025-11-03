import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import { useCart } from '../contexts/CartContext'

export default function ProductCard({ product }) {
  const { addToCart } = useCart()
  const [added, setAdded] = useState(false)

  const handleAddToCart = (e) => {
    e.preventDefault()
    addToCart(product, 1)
    setAdded(true)
    setTimeout(() => setAdded(false), 2000)
  }

  return (
    <div className="product-card">
      <Link to={`/product/${product.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
        <img src={product.image || '/assets/placeholder.svg'} alt={product.name} />
        <div className="product-body">
          <h3>{product.name}</h3>
          <p style={{ 
            color: 'var(--text-secondary)', 
            fontSize: '0.85rem', 
            marginBottom: '1rem',
            minHeight: '3em',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            display: '-webkit-box',
            WebkitLineClamp: 2,
            WebkitBoxOrient: 'vertical'
          }}>
            {product.description || 'Produit technologique de pointe'}
          </p>
          <p className="price">{product.price ? `${product.price} €` : '—'}</p>
        </div>
      </Link>
      
      <div style={{ padding: '0 1.25rem 1.25rem 1.25rem', display: 'flex', gap: '0.5rem' }}>
        <button 
          onClick={handleAddToCart}
          className="btn"
          style={{ 
            flex: 1, 
            marginTop: 0,
            fontSize: '0.9rem',
            padding: '0.6rem'
          }}
        >
          {added ? '✓ Ajouté' : '+ Panier'}
        </button>
        <Link 
          to={`/product/${product.id}`}
          className="btn btn-secondary"
          style={{ 
            marginTop: 0,
            fontSize: '0.9rem',
            padding: '0.6rem 1rem'
          }}
        >
          Détails
        </Link>
      </div>
    </div>
  )
}
