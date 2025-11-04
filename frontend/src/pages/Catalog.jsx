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
    <>
      <section className="hero">
        <div className="hero-content">
          <h1>
            L’innovation d’aujourd’hui,
            <br /> le standard de demain.
          </h1>
          <p>
            Explorez notre sélection de technologies futuristes conçues pour booster votre quotidien.
            Des performances de pointe, un design soigné et une expérience unique.
          </p>
          <div className="hero-actions">
            <a href="#catalog" className="btn">Découvrir les produits</a>
            <a href="#why-us" className="btn btn-secondary">Pourquoi EcomNova ?</a>
          </div>
        </div>
      </section>

      <section id="why-us" className="value-props">
        <div className="value-item">
          <span className="value-title">Qualité premium</span>
          <span className="value-desc">Matériaux haut de gamme et tests rigoureux</span>
        </div>
        <div className="value-item">
          <span className="value-title">Innovation continue</span>
          <span className="value-desc">R&D permanente et mises à jour régulières</span>
        </div>
        <div className="value-item">
          <span className="value-title">Support expert</span>
          <span className="value-desc">Assistance 7j/7 par des spécialistes</span>
        </div>
      </section>

      <h2 id="catalog" className="section-title">Catalogue</h2>
      <div className="catalog">
        {products.map((p) => (
          <ProductCard key={p.id} product={p} />
        ))}
      </div>
    </>
  )
}
