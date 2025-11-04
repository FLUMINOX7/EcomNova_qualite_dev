import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNotify } from '../contexts/NotificationContext'
import { useNavigate } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function Orders() {
  const { user } = useAuth()
  const { show } = useNotify()
  const navigate = useNavigate()
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(true)
  const [expandedOrder, setExpandedOrder] = useState(null)

  useEffect(() => {
    if (!user) {
      navigate('/auth')
      return
    }
    fetchOrders()
  }, [user, navigate])

  async function fetchOrders() {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/orders`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) throw new Error('Failed to fetch orders')
      const data = await res.json()
      setOrders(data)
    } catch (err) {
      show(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  async function cancelOrder(orderId) {
    if (!confirm('Êtes-vous sûr de vouloir annuler cette commande ?')) return
    
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/orders/${orderId}/cancel`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      })
      
      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.detail || 'Failed to cancel order')
      }
      
      show('Commande annulée avec succès', 'success')
      fetchOrders()
    } catch (err) {
      show(err.message, 'error')
    }
  }

  function getStatusColor(status) {
    const colors = {
      CREE: '#fbbf24',
      VALIDEE: '#60a5fa',
      PAYEE: '#34d399',
      EXPEDIEE: '#a78bfa',
      LIVREE: '#10b981',
      ANNULEE: '#ef4444',
      REMBOURSEE: '#f97316'
    }
    return colors[status] || '#6b7280'
  }

  function getStatusLabel(status) {
    const labels = {
      CREE: 'Créée',
      VALIDEE: 'Validée',
      PAYEE: 'Payée',
      EXPEDIEE: 'Expédiée',
      LIVREE: 'Livrée',
      ANNULEE: 'Annulée',
      REMBOURSEE: 'Remboursée'
    }
    return labels[status] || status
  }

  function canCancel(order) {
    return !['EXPEDIEE', 'LIVREE', 'ANNULEE', 'REMBOURSEE'].includes(order.status)
  }

  if (loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <p style={{ color: 'var(--galaxy-cyan)' }}>Chargement...</p>
      </div>
    )
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ 
        fontSize: '2.5rem', 
        marginBottom: '2rem',
        background: 'linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple))',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent'
      }}>
        Mes Commandes
      </h1>

      {orders.length === 0 ? (
        <div style={{
          padding: '3rem',
          textAlign: 'center',
          background: 'rgba(255,255,255,0.02)',
          border: '1px solid var(--border-glow)',
          borderRadius: '12px'
        }}>
          <p style={{ color: 'var(--text-dim)', marginBottom: '1rem' }}>
            Aucune commande pour le moment
          </p>
          <button
            onClick={() => navigate('/catalog')}
            style={{
              padding: '0.75rem 1.5rem',
              background: 'linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple))',
              border: 'none',
              borderRadius: '8px',
              color: 'white',
              fontSize: '1rem',
              cursor: 'pointer'
            }}
          >
            Découvrir nos produits
          </button>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {orders.map(order => (
            <div
              key={order.id}
              style={{
                background: 'rgba(255,255,255,0.02)',
                border: '1px solid var(--border-glow)',
                borderRadius: '12px',
                padding: '1.5rem',
                transition: 'all 0.3s ease'
              }}
            >
              {/* Header */}
              <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                marginBottom: '1rem',
                flexWrap: 'wrap',
                gap: '1rem'
              }}>
                <div>
                  <p style={{ color: 'var(--text-dim)', fontSize: '0.875rem' }}>
                    Commande #{order.id.substring(0, 8)}
                  </p>
                  <p style={{ color: 'var(--text-dim)', fontSize: '0.875rem' }}>
                    {new Date(order.created_at * 1000).toLocaleDateString('fr-FR', {
                      day: 'numeric',
                      month: 'long',
                      year: 'numeric'
                    })}
                  </p>
                </div>
                
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                  <span style={{
                    padding: '0.5rem 1rem',
                    borderRadius: '20px',
                    backgroundColor: getStatusColor(order.status) + '20',
                    color: getStatusColor(order.status),
                    fontSize: '0.875rem',
                    fontWeight: '600'
                  }}>
                    {getStatusLabel(order.status)}
                  </span>
                  
                  <button
                    onClick={() => setExpandedOrder(expandedOrder === order.id ? null : order.id)}
                    style={{
                      padding: '0.5rem 1rem',
                      background: 'rgba(255,255,255,0.05)',
                      border: '1px solid var(--border-glow)',
                      borderRadius: '8px',
                      color: 'var(--galaxy-cyan)',
                      cursor: 'pointer'
                    }}
                  >
                    {expandedOrder === order.id ? 'Masquer' : 'Détails'}
                  </button>
                </div>
              </div>

              {/* Total */}
              <div style={{
                fontSize: '1.5rem',
                fontWeight: '600',
                color: 'white',
                marginBottom: '1rem'
              }}>
                {(order.total_price_cents / 100).toFixed(2)} €
              </div>

              {/* Expanded Details */}
              {expandedOrder === order.id && (
                <div style={{
                  marginTop: '1.5rem',
                  paddingTop: '1.5rem',
                  borderTop: '1px solid var(--border-glow)'
                }}>
                  {/* Items */}
                  <h3 style={{ 
                    fontSize: '1.125rem', 
                    marginBottom: '1rem',
                    color: 'var(--galaxy-cyan)'
                  }}>
                    Articles
                  </h3>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', marginBottom: '1.5rem' }}>
                    {order.items.map(item => (
                      <div key={item.id} style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        padding: '0.75rem',
                        background: 'rgba(255,255,255,0.02)',
                        borderRadius: '8px'
                      }}>
                        <div>
                          <p style={{ fontWeight: '500' }}>{item.name}</p>
                          <p style={{ color: 'var(--text-dim)', fontSize: '0.875rem' }}>
                            {(item.unit_price_cents / 100).toFixed(2)} € × {item.quantity}
                          </p>
                        </div>
                        <p style={{ fontWeight: '600', color: 'var(--galaxy-cyan)' }}>
                          {(item.total_price_cents / 100).toFixed(2)} €
                        </p>
                      </div>
                    ))}
                  </div>

                  {/* Tracking */}
                  {order.status === 'EXPEDIEE' && (
                    <div style={{
                      padding: '1rem',
                      background: 'rgba(167, 139, 250, 0.1)',
                      border: '1px solid rgba(167, 139, 250, 0.3)',
                      borderRadius: '8px',
                      marginBottom: '1rem'
                    }}>
                      <p style={{ color: 'var(--galaxy-purple)', fontWeight: '600', marginBottom: '0.5rem' }}>
                        📦 Colis expédié
                      </p>
                      <p style={{ color: 'var(--text-dim)', fontSize: '0.875rem' }}>
                        Numéro de suivi disponible prochainement
                      </p>
                    </div>
                  )}

                  {/* Actions */}
                  {canCancel(order) && (
                    <button
                      onClick={() => cancelOrder(order.id)}
                      style={{
                        padding: '0.75rem 1.5rem',
                        background: 'transparent',
                        border: '1px solid #ef4444',
                        borderRadius: '8px',
                        color: '#ef4444',
                        cursor: 'pointer',
                        fontSize: '0.875rem',
                        fontWeight: '600',
                        transition: 'all 0.3s ease'
                      }}
                      onMouseEnter={e => e.target.style.background = 'rgba(239, 68, 68, 0.1)'}
                      onMouseLeave={e => e.target.style.background = 'transparent'}
                    >
                      Annuler la commande
                    </button>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
