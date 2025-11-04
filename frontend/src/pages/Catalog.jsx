import React, { useEffect, useState } from 'react'
import ProductCard from '../components/ProductCard'
import { fetchProducts } from '../utils/api'

export default function Catalog() {
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedCategory, setSelectedCategory] = useState('all')
  const [sortBy, setSortBy] = useState('name')

  useEffect(() => {
    let mounted = true
    fetchProducts().then((data) => {
      if (mounted) setProducts(data || [])
      setLoading(false)
    })
    return () => (mounted = false)
  }, [])

  // Extract unique categories from products
  const categories = ['all', ...new Set(products.map(p => {
    // Extract category from description or use a default
    const match = p.description?.match(/(?:Processeur|Casque|Interface|Écran|Drone|Suite|Scanner|Station|Système|Hub|Tracker|Assistant)/i)
    if (match) {
      const keyword = match[0].toLowerCase()
      if (keyword.includes('processeur')) return 'Computing'
      if (keyword.includes('casque')) return 'VR'
      if (keyword.includes('interface')) return 'Neural Tech'
      if (keyword.includes('écran')) return 'Displays'
      if (keyword.includes('drone')) return 'Drones'
      if (keyword.includes('suite')) return 'Security'
      if (keyword.includes('scanner')) return 'Medical'
      if (keyword.includes('station')) return 'Energy'
      if (keyword.includes('système')) return 'Audio'
      if (keyword.includes('hub')) return 'Networking'
      if (keyword.includes('tracker')) return 'Health'
      if (keyword.includes('assistant')) return 'AI'
    }
    return 'Other'
  }).filter(Boolean))]

  // Filter and sort products
  const filteredProducts = products
    .filter(p => {
      const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           p.description?.toLowerCase().includes(searchTerm.toLowerCase())
      const matchesCategory = selectedCategory === 'all' || getCategoryForProduct(p) === selectedCategory
      return matchesSearch && matchesCategory
    })
    .sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name)
      if (sortBy === 'price-asc') return a.price_cents - b.price_cents
      if (sortBy === 'price-desc') return b.price_cents - a.price_cents
      if (sortBy === 'stock') return b.stock_qty - a.stock_qty
      return 0
    })

  function getCategoryForProduct(p) {
    const match = p.description?.match(/(?:Processeur|Casque|Interface|Écran|Drone|Suite|Scanner|Station|Système|Hub|Tracker|Assistant)/i)
    if (match) {
      const keyword = match[0].toLowerCase()
      if (keyword.includes('processeur')) return 'Computing'
      if (keyword.includes('casque')) return 'VR'
      if (keyword.includes('interface')) return 'Neural Tech'
      if (keyword.includes('écran')) return 'Displays'
      if (keyword.includes('drone')) return 'Drones'
      if (keyword.includes('suite')) return 'Security'
      if (keyword.includes('scanner')) return 'Medical'
      if (keyword.includes('station')) return 'Energy'
      if (keyword.includes('système')) return 'Audio'
      if (keyword.includes('hub')) return 'Networking'
      if (keyword.includes('tracker')) return 'Health'
      if (keyword.includes('assistant')) return 'AI'
    }
    return 'Other'
  }

  function getCategoryIcon(category) {
    const icons = {
      'Computing': '💻',
      'VR': '🥽',
      'Neural Tech': '🧠',
      'Displays': '🖥️',
      'Drones': '🚁',
      'Security': '🔒',
      'Medical': '⚕️',
      'Energy': '⚡',
      'Audio': '🔊',
      'Networking': '🌐',
      'Health': '❤️',
      'AI': '🤖',
      'Other': '📦',
      'all': '🌟'
    }
    return icons[category] || '📦'
  }

  if (loading) {
    return (
      <div style={{ 
        padding: '3rem', 
        textAlign: 'center',
        minHeight: '60vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div>
          <div style={{
            width: '50px',
            height: '50px',
            border: '3px solid var(--border-glow)',
            borderTop: '3px solid var(--galaxy-cyan)',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 1rem'
          }}></div>
          <p style={{ color: 'var(--galaxy-cyan)' }}>Chargement du catalogue...</p>
        </div>
      </div>
    )
  }

  return (
    <>
      <section className="hero">
        <div className="hero-content">
          <h1>
            L'innovation d'aujourd'hui,
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

      <div id="catalog" style={{ 
        maxWidth: '1400px', 
        margin: '0 auto', 
        padding: '2rem 1rem' 
      }}>
        {/* Search and Filters Bar */}
        <div style={{
          background: 'rgba(255,255,255,0.02)',
          border: '1px solid var(--border-glow)',
          borderRadius: '16px',
          padding: '2rem',
          marginBottom: '2rem',
          backdropFilter: 'blur(10px)'
        }}>
          <h2 style={{ 
            fontSize: '2rem',
            marginBottom: '1.5rem',
            background: 'linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple))',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            🛍️ Catalogue Produits
          </h2>

          {/* Search Bar */}
          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ position: 'relative' }}>
              <input
                type="text"
                placeholder="🔍 Rechercher un produit..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                style={{
                  width: '100%',
                  padding: '1rem 1rem 1rem 3rem',
                  background: 'rgba(255,255,255,0.05)',
                  border: '1px solid var(--border-glow)',
                  borderRadius: '12px',
                  color: 'white',
                  fontSize: '1rem',
                  outline: 'none',
                  transition: 'all 0.3s ease'
                }}
                onFocus={(e) => e.target.style.borderColor = 'var(--galaxy-cyan)'}
                onBlur={(e) => e.target.style.borderColor = 'var(--border-glow)'}
              />
              <span style={{
                position: 'absolute',
                left: '1rem',
                top: '50%',
                transform: 'translateY(-50%)',
                fontSize: '1.2rem'
              }}>🔍</span>
            </div>
          </div>

          {/* Categories Filter */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '0.75rem',
              color: 'var(--text-dim)',
              fontSize: '0.875rem',
              fontWeight: '600'
            }}>
              CATÉGORIES
            </label>
            <div style={{
              display: 'flex',
              gap: '0.75rem',
              flexWrap: 'wrap'
            }}>
              {categories.map(cat => (
                <button
                  key={cat}
                  onClick={() => setSelectedCategory(cat)}
                  style={{
                    padding: '0.75rem 1.5rem',
                    background: selectedCategory === cat 
                      ? 'linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple))'
                      : 'rgba(255,255,255,0.05)',
                    border: selectedCategory === cat
                      ? 'none'
                      : '1px solid var(--border-glow)',
                    borderRadius: '25px',
                    color: 'white',
                    fontSize: '0.875rem',
                    fontWeight: '600',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}
                  onMouseEnter={(e) => {
                    if (selectedCategory !== cat) {
                      e.target.style.background = 'rgba(255,255,255,0.08)'
                      e.target.style.transform = 'translateY(-2px)'
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (selectedCategory !== cat) {
                      e.target.style.background = 'rgba(255,255,255,0.05)'
                      e.target.style.transform = 'translateY(0)'
                    }
                  }}
                >
                  <span>{getCategoryIcon(cat)}</span>
                  <span>{cat === 'all' ? 'Tous' : cat}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Sort Dropdown */}
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '1rem',
            flexWrap: 'wrap',
            justifyContent: 'space-between'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
              <label style={{ 
                color: 'var(--text-dim)',
                fontSize: '0.875rem',
                fontWeight: '600'
              }}>
                TRIER PAR
              </label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                style={{
                  padding: '0.75rem 1rem',
                  background: 'rgba(255,255,255,0.05)',
                  border: '1px solid var(--border-glow)',
                  borderRadius: '8px',
                  color: 'white',
                  fontSize: '0.875rem',
                  cursor: 'pointer',
                  outline: 'none'
                }}
              >
                <option value="name">Nom A-Z</option>
                <option value="price-asc">Prix croissant</option>
                <option value="price-desc">Prix décroissant</option>
                <option value="stock">Stock disponible</option>
              </select>
            </div>

            <div style={{ 
              color: 'var(--text-dim)',
              fontSize: '0.875rem'
            }}>
              {filteredProducts.length} produit{filteredProducts.length > 1 ? 's' : ''} trouvé{filteredProducts.length > 1 ? 's' : ''}
            </div>
          </div>
        </div>

        {/* Products Grid */}
        {filteredProducts.length === 0 ? (
          <div style={{
            padding: '4rem 2rem',
            textAlign: 'center',
            background: 'rgba(255,255,255,0.02)',
            border: '1px solid var(--border-glow)',
            borderRadius: '16px'
          }}>
            <div style={{ fontSize: '4rem', marginBottom: '1rem' }}>🔍</div>
            <h3 style={{ marginBottom: '0.5rem' }}>Aucun produit trouvé</h3>
            <p style={{ color: 'var(--text-dim)' }}>
              Essayez de modifier vos critères de recherche ou de filtre
            </p>
          </div>
        ) : (
          <div className="catalog">
            {filteredProducts.map((p) => (
              <ProductCard key={p.id} product={p} />
            ))}
          </div>
        )}
      </div>

      <style>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </>
  )
}
