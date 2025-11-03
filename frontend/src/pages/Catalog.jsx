import React, { useEffect, useState } from 'react'
import ProductCard from '../components/ProductCard'
import { fetchProducts } from '../utils/api'

export default function Catalog() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let mounted = true
    fetchProducts().then((data) => {
      if (mounted) setProducts(data || [])
      setLoading(false)
    })
    return () => (mounted = false)
  }, [])

  if (loading) return <div>Chargement...</div>
  if (!products.length) return <div>Aucun produit trouvé.</div>

  return (
    <div className="catalog">
      {products.map((p) => (
        <ProductCard key={p.id} product={p} />
      ))}
    </div>
  )
}
