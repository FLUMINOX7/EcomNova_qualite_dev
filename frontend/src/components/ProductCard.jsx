import React from 'react'
import { Link } from 'react-router-dom'

export default function ProductCard({ product }) {
  return (
    <div className="product-card">
      <img src={product.image || '/assets/placeholder.png'} alt={product.name} />
      <div className="product-body">
        <h3>{product.name}</h3>
        <p className="price">{product.price ? `${product.price} €` : '—'}</p>
        <Link to={`/product/${product.id}`} className="btn">Voir</Link>
      </div>
    </div>
  )
}
