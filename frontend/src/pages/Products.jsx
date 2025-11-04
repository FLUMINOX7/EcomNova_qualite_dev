import React, { useEffect, useState } from 'react'
import ProductCard from '../components/ProductCard'
import { fetchProducts } from '../utils/api'

export default function Products() {
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
      <div className="loading-container">
        <div className="loading-content">
          <div className="loading-spinner"></div>
          <p>Chargement du catalogue...</p>
        </div>
      </div>
    )
  }

  return (
    <>
      {/* Header Section */}
      <section className="products-header">
        <div className="container">
          <div className="header-content">
            <h1 className="page-title">
              <span className="gradient-text">🛍️ Catalogue Produits</span>
            </h1>
            <p className="page-description">
              Découvrez notre sélection complète de technologies innovantes.
              {products.length} produits de haute qualité vous attendent.
            </p>
          </div>
        </div>
      </section>

      <div className="products-container">
        <div className="container">
          {/* Filters Panel */}
          <div className="filters-panel">
            {/* Search Bar */}
            <div className="search-section">
              <div className="search-wrapper">
                <input
                  type="text"
                  placeholder="🔍 Rechercher un produit..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="search-input"
                />
                <div className="search-icon">🔍</div>
              </div>
            </div>

            {/* Categories Filter */}
            <div className="filter-section">
              <label className="filter-label">CATÉGORIES</label>
              <div className="categories-grid">
                {categories.map(cat => (
                  <button
                    key={cat}
                    onClick={() => setSelectedCategory(cat)}
                    className={`category-btn ${selectedCategory === cat ? 'active' : ''}`}
                  >
                    <span className="category-icon">{getCategoryIcon(cat)}</span>
                    <span className="category-name">{cat === 'all' ? 'Tous' : cat}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Sort and Results */}
            <div className="controls-section">
              <div className="sort-wrapper">
                <label className="filter-label">TRIER PAR</label>
                <select
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value)}
                  className="sort-select"
                >
                  <option value="name">Nom A-Z</option>
                  <option value="price-asc">Prix croissant</option>
                  <option value="price-desc">Prix décroissant</option>
                  <option value="stock">Stock disponible</option>
                </select>
              </div>

              <div className="results-count">
                <span className="count-badge">
                  {filteredProducts.length} produit{filteredProducts.length > 1 ? 's' : ''} trouvé{filteredProducts.length > 1 ? 's' : ''}
                </span>
              </div>
            </div>
          </div>

          {/* Products Grid */}
          {filteredProducts.length === 0 ? (
            <div className="no-results">
              <div className="no-results-icon">🔍</div>
              <h3>Aucun produit trouvé</h3>
              <p>Essayez de modifier vos critères de recherche ou de filtre</p>
              <button 
                onClick={() => {
                  setSearchTerm('')
                  setSelectedCategory('all')
                }}
                className="btn btn-primary"
              >
                Réinitialiser les filtres
              </button>
            </div>
          ) : (
            <div className="products-grid">
              {filteredProducts.map((product, index) => (
                <div 
                  key={product.id}
                  className="product-wrapper"
                  style={{
                    animationDelay: `${index * 100}ms`
                  }}
                >
                  <ProductCard product={product} />
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      <style>{`
        /* Loading */
        .loading-container {
          padding: 3rem;
          text-align: center;
          min-height: 60vh;
          display: flex;
          align-items: center;
          justify-content: center;
          background: var(--galaxy-dark);
        }

        .loading-content {
          max-width: 300px;
        }

        .loading-spinner {
          width: 50px;
          height: 50px;
          border: 3px solid var(--border-glow);
          border-top: 3px solid var(--galaxy-cyan);
          border-radius: 50%;
          animation: spin 1s linear infinite;
          margin: 0 auto 1rem;
        }

        .loading-content p {
          color: var(--galaxy-cyan);
          font-size: 1.1rem;
        }

        /* Header */
        .products-header {
          background: linear-gradient(135deg, var(--galaxy-dark) 0%, var(--galaxy-deep) 100%);
          padding: 3rem 0 2rem;
          border-bottom: 1px solid var(--border-glow);
        }

        .container {
          max-width: 1400px;
          margin: 0 auto;
          padding: 0 2rem;
        }

        .header-content {
          text-align: center;
          max-width: 800px;
          margin: 0 auto;
        }

        .page-title {
          font-size: clamp(2rem, 4vw, 3rem);
          margin-bottom: 1rem;
          animation: slideInUp 0.8s ease-out;
        }

        .gradient-text {
          background: linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .page-description {
          font-size: 1.1rem;
          color: var(--text-dim);
          line-height: 1.6;
          animation: slideInUp 0.8s ease-out 0.2s both;
        }

        /* Products Container */
        .products-container {
          background: var(--galaxy-dark);
          min-height: 80vh;
          padding: 2rem 0;
        }

        /* Filters Panel */
        .filters-panel {
          background: rgba(255,255,255,0.02);
          border: 1px solid var(--border-glow);
          border-radius: 20px;
          padding: 2rem;
          margin-bottom: 2rem;
          backdrop-filter: blur(10px);
          animation: slideInUp 0.8s ease-out 0.4s both;
        }

        /* Search Section */
        .search-section {
          margin-bottom: 2rem;
        }

        .search-wrapper {
          position: relative;
          max-width: 500px;
          margin: 0 auto;
        }

        .search-input {
          width: 100%;
          padding: 1rem 1rem 1rem 3.5rem;
          background: rgba(255,255,255,0.05);
          border: 1px solid var(--border-glow);
          border-radius: 50px;
          color: white;
          font-size: 1rem;
          outline: none;
          transition: all 0.3s ease;
        }

        .search-input:focus {
          border-color: var(--galaxy-cyan);
          box-shadow: 0 0 20px rgba(0, 212, 255, 0.2);
          background: rgba(255,255,255,0.08);
        }

        .search-icon {
          position: absolute;
          left: 1.25rem;
          top: 50%;
          transform: translateY(-50%);
          font-size: 1.2rem;
          color: var(--text-dim);
        }

        /* Filter Section */
        .filter-section {
          margin-bottom: 2rem;
        }

        .filter-label {
          display: block;
          margin-bottom: 1rem;
          color: var(--text-dim);
          font-size: 0.875rem;
          font-weight: 600;
          text-transform: uppercase;
          letter-spacing: 1px;
        }

        .categories-grid {
          display: flex;
          gap: 0.75rem;
          flex-wrap: wrap;
          justify-content: center;
        }

        .category-btn {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          padding: 0.75rem 1.5rem;
          background: rgba(255,255,255,0.05);
          border: 1px solid var(--border-glow);
          border-radius: 50px;
          color: white;
          font-size: 0.875rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
          text-decoration: none;
        }

        .category-btn:hover {
          background: rgba(255,255,255,0.1);
          transform: translateY(-2px);
          border-color: var(--galaxy-cyan);
        }

        .category-btn.active {
          background: linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple));
          border: none;
          box-shadow: 0 4px 15px rgba(0, 212, 255, 0.3);
        }

        .category-icon {
          font-size: 1rem;
        }

        /* Controls Section */
        .controls-section {
          display: flex;
          align-items: center;
          justify-content: space-between;
          flex-wrap: wrap;
          gap: 1rem;
        }

        .sort-wrapper {
          display: flex;
          align-items: center;
          gap: 1rem;
        }

        .sort-select {
          padding: 0.75rem 1rem;
          background: rgba(255,255,255,0.05);
          border: 1px solid var(--border-glow);
          border-radius: 10px;
          color: white;
          font-size: 0.875rem;
          cursor: pointer;
          outline: none;
          transition: all 0.3s ease;
        }

        .sort-select:focus {
          border-color: var(--galaxy-cyan);
        }

        .sort-select option {
          background: var(--galaxy-deep);
          color: white;
        }

        .results-count {
          display: flex;
          align-items: center;
        }

        .count-badge {
          background: linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple));
          color: white;
          padding: 0.5rem 1rem;
          border-radius: 20px;
          font-size: 0.875rem;
          font-weight: 600;
        }

        /* No Results */
        .no-results {
          padding: 4rem 2rem;
          text-align: center;
          background: rgba(255,255,255,0.02);
          border: 1px solid var(--border-glow);
          border-radius: 20px;
          margin-top: 2rem;
        }

        .no-results-icon {
          font-size: 4rem;
          margin-bottom: 1rem;
          opacity: 0.5;
        }

        .no-results h3 {
          margin-bottom: 0.5rem;
          color: white;
        }

        .no-results p {
          color: var(--text-dim);
          margin-bottom: 2rem;
        }

        .btn {
          display: inline-flex;
          align-items: center;
          gap: 0.5rem;
          padding: 1rem 2rem;
          border-radius: 50px;
          text-decoration: none;
          font-weight: 600;
          transition: all 0.3s ease;
          border: none;
          cursor: pointer;
          font-size: 1rem;
        }

        .btn-primary {
          background: linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple));
          color: white;
          box-shadow: 0 4px 20px rgba(0, 212, 255, 0.3);
        }

        .btn-primary:hover {
          transform: translateY(-3px);
          box-shadow: 0 8px 30px rgba(0, 212, 255, 0.4);
        }

        /* Products Grid */
        .products-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
          gap: 2rem;
          margin-top: 2rem;
        }

        .product-wrapper {
          animation: slideInUp 0.6s ease-out both;
        }

        /* Animations */
        @keyframes slideInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        /* Responsive */
        @media (max-width: 768px) {
          .categories-grid {
            justify-content: flex-start;
          }
          
          .controls-section {
            flex-direction: column;
            align-items: flex-start;
          }
          
          .products-grid {
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 1.5rem;
          }
          
          .filters-panel {
            padding: 1.5rem;
          }
        }

        @media (max-width: 480px) {
          .categories-grid {
            flex-direction: column;
          }
          
          .category-btn {
            justify-content: center;
          }
          
          .products-grid {
            grid-template-columns: 1fr;
          }
        }
      `}</style>
    </>
  )
}