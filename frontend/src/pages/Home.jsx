import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { getStats } from '../utils/api'

// Hook pour animer les compteurs
function useCounter(target, duration = 2000) {
  const [count, setCount] = useState(0)
  
  useEffect(() => {
    let startTime
    const animate = (timestamp) => {
      if (!startTime) startTime = timestamp
      const progress = Math.min((timestamp - startTime) / duration, 1)
      setCount(Math.floor(progress * target))
      if (progress < 1) {
        requestAnimationFrame(animate)
      }
    }
    requestAnimationFrame(animate)
  }, [target, duration])
  
  return count
}

// Composant Stat Card avec animation
function StatCard({ icon, title, value, description, delay = 0 }) {
  const animatedValue = useCounter(value, 2000 + delay)
  
  return (
    <div 
      className="stat-card"
      style={{
        animationDelay: `${delay}ms`
      }}
    >
      <div className="stat-icon">{icon}</div>
      <div className="stat-content">
        <h3 className="stat-value">{animatedValue.toLocaleString()}</h3>
        <p className="stat-title">{title}</p>
        <p className="stat-description">{description}</p>
      </div>
    </div>
  )
}

// Composant Feature Card
function FeatureCard({ icon, title, description, delay = 0 }) {
  return (
    <div 
      className="feature-card"
      style={{
        animationDelay: `${delay}ms`
      }}
    >
      <div className="feature-icon">{icon}</div>
      <h3>{title}</h3>
      <p>{description}</p>
    </div>
  )
}

export default function Home() {
  const [stats, setStats] = useState({
    products: 0,
    customers: 0,
    orders: 0,
    satisfaction: 0
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Charger les statistiques réelles depuis l'API
    const loadStats = async () => {
      try {
        const statsData = await getStats()
        setStats(statsData)
      } catch (error) {
        console.error('Erreur lors du chargement des stats:', error)
        // Utiliser des données de fallback
        setStats({
          products: 29,
          customers: 1247,
          orders: 892,
          satisfaction: 98
        })
      } finally {
        setLoading(false)
      }
    }

    loadStats()
  }, [])

  return (
    <>
      {/* Hero Section */}
      <section className="hero-modern">
        <div className="hero-bg">
          <div className="floating-particles"></div>
        </div>
        <div className="hero-content">
          <h1 className="hero-title">
            <span className="gradient-text">L'innovation d'aujourd'hui,</span>
            <br />
            <span className="hero-subtitle">le standard de demain.</span>
          </h1>
          <p className="hero-description">
            Explorez notre sélection de technologies futuristes conçues pour booster votre quotidien.
            Des performances de pointe, un design soigné et une expérience unique.
          </p>
          <div className="hero-actions">
            <Link to="/products" className="btn btn-primary">
              <span>🚀</span>
              Découvrir les produits
            </Link>
            <a href="#features" className="btn btn-secondary">
              <span>💡</span>
              Pourquoi EcomNova ?
            </a>
          </div>
        </div>
      </section>

      {/* Statistics Section */}
      <section className="stats-section">
        <div className="container">
          <h2 className="section-title">
            📊 EcomNova en chiffres
          </h2>
          <div className="stats-grid">
            <StatCard
              icon="🛍️"
              title="Produits disponibles"
              value={stats.products}
              description="Technologies de pointe"
              delay={0}
            />
            <StatCard
              icon="👥"
              title="Clients satisfaits"
              value={stats.customers}
              description="Dans le monde entier"
              delay={200}
            />
            <StatCard
              icon="📦"
              title="Commandes livrées"
              value={stats.orders}
              description="Livraison express"
              delay={400}
            />
            <StatCard
              icon="⭐"
              title="Satisfaction client"
              value={stats.satisfaction}
              description="% de recommandation"
              delay={600}
            />
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="features-section">
        <div className="container">
          <h2 className="section-title">
            ✨ Pourquoi choisir EcomNova ?
          </h2>
          <div className="features-grid">
            <FeatureCard
              icon="🔬"
              title="Innovation continue"
              description="R&D permanente et technologies de pointe pour rester à la pointe de l'innovation."
              delay={0}
            />
            <FeatureCard
              icon="🛡️"
              title="Qualité premium"
              description="Matériaux haut de gamme et tests rigoureux pour garantir la durabilité."
              delay={200}
            />
            <FeatureCard
              icon="🚀"
              title="Livraison rapide"
              description="Expédition sous 24h et livraison express dans le monde entier."
              delay={400}
            />
            <FeatureCard
              icon="💬"
              title="Support expert"
              description="Assistance 7j/7 par des spécialistes techniques expérimentés."
              delay={600}
            />
            <FeatureCard
              icon="🔒"
              title="Paiement sécurisé"
              description="Transactions cryptées et protection des données personnelles."
              delay={800}
            />
            <FeatureCard
              icon="♻️"
              title="Éco-responsable"
              description="Engagement environnemental et emballages recyclables."
              delay={1000}
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="container">
          <div className="cta-content">
            <h2>Prêt à découvrir l'avenir ?</h2>
            <p>Rejoignez des milliers de clients qui ont déjà fait le choix de l'innovation</p>
            <div className="cta-actions">
              <Link to="/products" className="btn btn-primary btn-large">
                <span>🛍️</span>
                Explorer le catalogue
              </Link>
              <Link to="/auth" className="btn btn-outline btn-large">
                <span>✨</span>
                Créer un compte
              </Link>
            </div>
          </div>
        </div>
      </section>

      <style>{`
        /* Hero Modern */
        .hero-modern {
          position: relative;
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          overflow: hidden;
          background: linear-gradient(135deg, var(--galaxy-dark) 0%, var(--galaxy-deep) 50%, var(--galaxy-blue) 100%);
        }

        .hero-bg {
          position: absolute;
          inset: 0;
          pointer-events: none;
        }

        .floating-particles {
          position: absolute;
          width: 100%;
          height: 100%;
          background-image: 
            radial-gradient(2px 2px at 20px 30px, var(--galaxy-cyan), transparent),
            radial-gradient(2px 2px at 40px 70px, var(--galaxy-purple), transparent),
            radial-gradient(1px 1px at 90px 40px, var(--galaxy-bright), transparent),
            radial-gradient(1px 1px at 130px 80px, var(--galaxy-cyan), transparent);
          background-repeat: repeat;
          background-size: 200px 200px;
          animation: float 20s linear infinite;
          opacity: 0.6;
        }

        @keyframes float {
          0% { transform: translate(0, 0) rotate(0deg); }
          33% { transform: translate(30px, -30px) rotate(120deg); }
          66% { transform: translate(-20px, 20px) rotate(240deg); }
          100% { transform: translate(0, 0) rotate(360deg); }
        }

        .hero-content {
          text-align: center;
          max-width: 800px;
          padding: 2rem;
          z-index: 2;
          position: relative;
        }

        .hero-title {
          font-size: clamp(2.5rem, 5vw, 4rem);
          font-weight: 700;
          margin-bottom: 1.5rem;
          line-height: 1.2;
          animation: slideInUp 1s ease-out;
        }

        .gradient-text {
          background: linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .hero-subtitle {
          display: inline-block;
          animation: slideInUp 1s ease-out 0.2s both;
        }

        .hero-description {
          font-size: 1.2rem;
          color: var(--text-dim);
          margin-bottom: 2.5rem;
          line-height: 1.6;
          animation: slideInUp 1s ease-out 0.4s both;
        }

        .hero-actions {
          display: flex;
          gap: 1rem;
          justify-content: center;
          flex-wrap: wrap;
          animation: slideInUp 1s ease-out 0.6s both;
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

        .btn-secondary {
          background: rgba(255, 255, 255, 0.1);
          color: white;
          border: 1px solid var(--border-glow);
          backdrop-filter: blur(10px);
        }

        .btn-secondary:hover {
          background: rgba(255, 255, 255, 0.2);
          transform: translateY(-3px);
        }

        .btn-outline {
          background: transparent;
          color: var(--galaxy-cyan);
          border: 2px solid var(--galaxy-cyan);
        }

        .btn-outline:hover {
          background: var(--galaxy-cyan);
          color: var(--galaxy-dark);
        }

        .btn-large {
          padding: 1.25rem 2.5rem;
          font-size: 1.1rem;
        }

        /* Stats Section */
        .stats-section {
          padding: 5rem 0;
          background: linear-gradient(180deg, rgba(26, 31, 58, 0.8) 0%, rgba(10, 14, 39, 0.9) 100%);
          position: relative;
        }

        .stats-section::before {
          content: '';
          position: absolute;
          inset: 0;
          background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="%23ffffff" stroke-width="0.1" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
          opacity: 0.3;
        }

        .container {
          max-width: 1200px;
          margin: 0 auto;
          padding: 0 2rem;
          position: relative;
          z-index: 2;
        }

        .section-title {
          text-align: center;
          font-size: 2.5rem;
          margin-bottom: 3rem;
          background: linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple));
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }

        .stats-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
          gap: 2rem;
        }

        .stat-card {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid var(--border-glow);
          border-radius: 20px;
          padding: 2rem;
          text-align: center;
          backdrop-filter: blur(10px);
          transition: all 0.3s ease;
          animation: slideInUp 0.8s ease-out both;
          position: relative;
          overflow: hidden;
        }

        .stat-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: -100%;
          width: 100%;
          height: 100%;
          background: linear-gradient(90deg, transparent, rgba(0, 212, 255, 0.1), transparent);
          transition: left 0.5s ease;
        }

        .stat-card:hover::before {
          left: 100%;
        }

        .stat-card:hover {
          transform: translateY(-10px);
          border-color: var(--galaxy-cyan);
          box-shadow: 0 10px 30px rgba(0, 212, 255, 0.2);
        }

        .stat-icon {
          font-size: 3rem;
          margin-bottom: 1rem;
          animation: bounce 2s infinite;
        }

        .stat-value {
          font-size: 3rem;
          font-weight: 700;
          color: var(--galaxy-cyan);
          margin-bottom: 0.5rem;
        }

        .stat-title {
          font-size: 1.2rem;
          font-weight: 600;
          margin-bottom: 0.5rem;
          color: white;
        }

        .stat-description {
          color: var(--text-dim);
          font-size: 0.9rem;
        }

        /* Features Section */
        .features-section {
          padding: 5rem 0;
          background: var(--galaxy-dark);
        }

        .features-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 2rem;
        }

        .feature-card {
          background: rgba(255, 255, 255, 0.03);
          border: 1px solid var(--border-glow);
          border-radius: 16px;
          padding: 2rem;
          transition: all 0.3s ease;
          animation: slideInUp 0.8s ease-out both;
          position: relative;
          overflow: hidden;
        }

        .feature-card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 3px;
          background: linear-gradient(90deg, var(--galaxy-cyan), var(--galaxy-purple));
          transform: scaleX(0);
          transition: transform 0.3s ease;
        }

        .feature-card:hover::before {
          transform: scaleX(1);
        }

        .feature-card:hover {
          transform: translateY(-5px);
          background: rgba(255, 255, 255, 0.08);
          border-color: var(--galaxy-cyan);
        }

        .feature-icon {
          font-size: 2.5rem;
          margin-bottom: 1rem;
          display: inline-block;
          animation: pulse 2s infinite;
        }

        .feature-card h3 {
          font-size: 1.3rem;
          margin-bottom: 1rem;
          color: var(--galaxy-cyan);
        }

        .feature-card p {
          color: var(--text-dim);
          line-height: 1.6;
        }

        /* CTA Section */
        .cta-section {
          padding: 5rem 0;
          background: linear-gradient(135deg, var(--galaxy-deep) 0%, var(--galaxy-blue) 100%);
          text-align: center;
        }

        .cta-content h2 {
          font-size: 2.5rem;
          margin-bottom: 1rem;
          color: white;
        }

        .cta-content p {
          font-size: 1.2rem;
          color: var(--text-dim);
          margin-bottom: 2.5rem;
        }

        .cta-actions {
          display: flex;
          gap: 1rem;
          justify-content: center;
          flex-wrap: wrap;
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

        @keyframes bounce {
          0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
          }
          40% {
            transform: translateY(-10px);
          }
          60% {
            transform: translateY(-5px);
          }
        }

        @keyframes pulse {
          0% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.1);
          }
          100% {
            transform: scale(1);
          }
        }

        /* Responsive */
        @media (max-width: 768px) {
          .hero-title {
            font-size: 2.5rem;
          }
          
          .stats-grid {
            grid-template-columns: 1fr;
          }
          
          .features-grid {
            grid-template-columns: 1fr;
          }
          
          .hero-actions, .cta-actions {
            flex-direction: column;
            align-items: center;
          }
          
          .btn {
            width: 100%;
            max-width: 300px;
          }
        }
      `}</style>
    </>
  )
}