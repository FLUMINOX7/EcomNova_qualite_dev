import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNotify } from '../contexts/NotificationContext'
import { useNavigate } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export default function AdminDashboard() {
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
    if (!user.is_admin) {
      show('Accès réservé aux administrateurs', 'error')
      navigate('/')
      return
    }
    fetchAllOrders()
  }, [user, navigate])

  async function fetchAllOrders() {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/orders/admin/all`, {
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

  async function updateOrderStatus(orderId, newStatus) {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/orders/${orderId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ status: newStatus })
      })
      
      if (!res.ok) throw new Error('Failed to update status')
      
      show(`Statut mis à jour: ${newStatus}`, 'success')
      fetchAllOrders()
    } catch (err) {
      show(err.message, 'error')
    }
  }

  async function shipOrder(orderId) {
    if (!confirm('Expédier cette commande ?')) return
    
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/orders/${orderId}/ship`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      })
      
      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.detail || 'Failed to ship order')
      }
      
      show('Commande expédiée avec succès', 'success')
      fetchAllOrders()
    } catch (err) {
      show(err.message, 'error')
    }
  }

  async function markDelivered(orderId) {
    if (!confirm('Marquer cette commande comme livrée ?')) return
    
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/orders/${orderId}/deliver`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      })
      
      if (!res.ok) throw new Error('Failed to mark as delivered')
      
      show('Commande marquée comme livrée', 'success')
      fetchAllOrders()
    } catch (err) {
      show(err.message, 'error')
    }
  }

  async function refundOrder(orderId) {
    if (!confirm('⚠️ Rembourser cette commande ? Le stock sera restitué.')) return
    
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/orders/${orderId}/refund`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}` }
      })
      
      if (!res.ok) {
        const error = await res.json()
        throw new Error(error.detail || 'Failed to refund order')
      }
      
      show('Commande remboursée avec succès', 'success')
      fetchAllOrders()
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

  function getAvailableActions(order) {
    const actions = []
    
    if (order.status === 'CREE') {
      actions.push({ label: 'Valider', action: () => updateOrderStatus(order.id, 'VALIDEE'), color: '#60a5fa' })
    }
    
    if (order.status === 'PAYEE') {
      actions.push({ label: 'Expédier', action: () => shipOrder(order.id), color: '#a78bfa' })
    }
    
    if (order.status === 'EXPEDIEE') {
      actions.push({ label: 'Marquer livrée', action: () => markDelivered(order.id), color: '#10b981' })
    }
    
    if (['PAYEE', 'EXPEDIEE', 'LIVREE'].includes(order.status)) {
      actions.push({ label: 'Rembourser', action: () => refundOrder(order.id), color: '#f97316' })
    }
    
    return actions
  }

  if (loading) {
    return (
      <div style={{ padding: '2rem', textAlign: 'center' }}>
        <p style={{ color: 'var(--galaxy-cyan)' }}>Chargement...</p>
      </div>
    )
  }

  return (
    <div style={{ padding: '2rem', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '2rem'
      }}>
        <h1 style={{ 
          fontSize: '2.5rem',
          background: 'linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple))',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          🛡️ Admin Dashboard
        </h1>
        <div style={{ color: 'var(--text-dim)' }}>
          {orders.length} commande{orders.length > 1 ? 's' : ''}
        </div>
      </div>

      {/* Stats */}
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '1rem',
        marginBottom: '2rem'
      }}>
        {['CREE', 'PAYEE', 'EXPEDIEE', 'LIVREE'].map(status => {
          const count = orders.filter(o => o.status === status).length
          return (
            <div key={status} style={{
              padding: '1.5rem',
              background: 'rgba(255,255,255,0.02)',
              border: `1px solid ${getStatusColor(status)}40`,
              borderRadius: '12px',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '2rem', fontWeight: '700', color: getStatusColor(status) }}>
                {count}
              </div>
              <div style={{ color: 'var(--text-dim)', fontSize: '0.875rem', marginTop: '0.5rem' }}>
                {status}
              </div>
            </div>
          )
        })}
      </div>

      {/* Orders List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {orders.map(order => {
          const actions = getAvailableActions(order)
          
          return (
            <div
              key={order.id}
              style={{
                background: 'rgba(255,255,255,0.02)',
                border: '1px solid var(--border-glow)',
                borderRadius: '12px',
                padding: '1.5rem'
              }}
            >
              <div style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: '1rem'
              }}>
                <div>
                  <p style={{ fontWeight: '600', marginBottom: '0.25rem' }}>
                    #{order.id.substring(0, 8)} - User: {order.user_id.substring(0, 8)}
                  </p>
                  <p style={{ color: 'var(--text-dim)', fontSize: '0.875rem' }}>
                    {new Date(order.created_at * 1000).toLocaleString('fr-FR')}
                  </p>
                </div>
                
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'center', flexWrap: 'wrap' }}>
                  <span style={{
                    padding: '0.5rem 1rem',
                    borderRadius: '20px',
                    backgroundColor: getStatusColor(order.status) + '20',
                    color: getStatusColor(order.status),
                    fontSize: '0.875rem',
                    fontWeight: '600'
                  }}>
                    {order.status}
                  </span>
                  
                  <span style={{ fontWeight: '700', fontSize: '1.25rem' }}>
                    {(order.total_price_cents / 100).toFixed(2)} €
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

              {/* Expanded Details */}
              {expandedOrder === order.id && (
                <div style={{
                  marginTop: '1.5rem',
                  paddingTop: '1.5rem',
                  borderTop: '1px solid var(--border-glow)'
                }}>
                  {/* Items */}
                  <div style={{ marginBottom: '1.5rem' }}>
                    <h4 style={{ color: 'var(--galaxy-cyan)', marginBottom: '0.75rem' }}>Articles</h4>
                    {order.items.map(item => (
                      <div key={item.id} style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        padding: '0.5rem',
                        background: 'rgba(255,255,255,0.02)',
                        borderRadius: '6px',
                        marginBottom: '0.5rem'
                      }}>
                        <span>{item.name} × {item.quantity}</span>
                        <span>{(item.total_price_cents / 100).toFixed(2)} €</span>
                      </div>
                    ))}
                  </div>

                  {/* Actions */}
                  {actions.length > 0 && (
                    <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
                      {actions.map((action, idx) => (
                        <button
                          key={idx}
                          onClick={action.action}
                          style={{
                            padding: '0.75rem 1.5rem',
                            background: `linear-gradient(135deg, ${action.color}, ${action.color}dd)`,
                            border: 'none',
                            borderRadius: '8px',
                            color: 'white',
                            cursor: 'pointer',
                            fontSize: '0.875rem',
                            fontWeight: '600',
                            transition: 'all 0.3s ease'
                          }}
                          onMouseEnter={e => e.target.style.transform = 'translateY(-2px)'}
                          onMouseLeave={e => e.target.style.transform = 'translateY(0)'}
                        >
                          {action.label}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
