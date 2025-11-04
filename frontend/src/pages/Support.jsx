import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { useNotify } from '../contexts/NotificationContext'
import { useNavigate } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export default function Support() {
  const { user } = useAuth()
  const { show } = useNotify()
  const navigate = useNavigate()
  const [threads, setThreads] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedThread, setSelectedThread] = useState(null)
  const [newMessage, setNewMessage] = useState('')
  const [showNewThread, setShowNewThread] = useState(false)
  const [newThreadSubject, setNewThreadSubject] = useState('')
  const [newThreadMessage, setNewThreadMessage] = useState('')

  useEffect(() => {
    if (!user) {
      navigate('/auth')
      return
    }
    fetchThreads()
  }, [user, navigate])

  async function fetchThreads() {
    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/threads`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (!res.ok) throw new Error('Failed to fetch threads')
      const data = await res.json()
      setThreads(data)
    } catch (err) {
      show(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  async function createThread() {
    if (!newThreadSubject.trim() || !newThreadMessage.trim()) {
      show('Veuillez remplir tous les champs', 'error')
      return
    }

    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/threads`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          subject: newThreadSubject,
          initial_message: newThreadMessage
        })
      })

      if (!res.ok) throw new Error('Failed to create thread')

      const newThread = await res.json()
      setThreads([newThread, ...threads])
      setNewThreadSubject('')
      setNewThreadMessage('')
      setShowNewThread(false)
      setSelectedThread(newThread)
      show('Ticket créé avec succès', 'success')
    } catch (err) {
      show(err.message, 'error')
    }
  }

  async function sendMessage(threadId) {
    if (!newMessage.trim()) return

    try {
      const token = localStorage.getItem('token')
      const res = await fetch(`${API_BASE}/threads/${threadId}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ body: newMessage })
      })

      if (!res.ok) throw new Error('Failed to send message')

      setNewMessage('')
      // Refresh thread to get new message
      const threadRes = await fetch(`${API_BASE}/threads/${threadId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      const updatedThread = await threadRes.json()
      setSelectedThread(updatedThread)
      
      // Update thread in list
      setThreads(threads.map(t => t.id === threadId ? updatedThread : t))
      show('Message envoyé', 'success')
    } catch (err) {
      show(err.message, 'error')
    }
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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 style={{ 
          fontSize: '2.5rem',
          background: 'linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple))',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          💬 Support
        </h1>
        <button
          onClick={() => setShowNewThread(!showNewThread)}
          style={{
            padding: '0.75rem 1.5rem',
            background: 'linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple))',
            border: 'none',
            borderRadius: '8px',
            color: 'white',
            fontSize: '1rem',
            fontWeight: '600',
            cursor: 'pointer'
          }}
        >
          {showNewThread ? 'Annuler' : '+ Nouveau ticket'}
        </button>
      </div>

      {/* New Thread Form */}
      {showNewThread && (
        <div style={{
          background: 'rgba(255,255,255,0.02)',
          border: '1px solid var(--border-glow)',
          borderRadius: '12px',
          padding: '1.5rem',
          marginBottom: '2rem'
        }}>
          <h3 style={{ marginBottom: '1rem', color: 'var(--galaxy-cyan)' }}>Créer un nouveau ticket</h3>
          <input
            type="text"
            placeholder="Sujet"
            value={newThreadSubject}
            onChange={e => setNewThreadSubject(e.target.value)}
            style={{
              width: '100%',
              padding: '0.75rem',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid var(--border-glow)',
              borderRadius: '8px',
              color: 'white',
              marginBottom: '1rem'
            }}
          />
          <textarea
            placeholder="Décrivez votre problème..."
            value={newThreadMessage}
            onChange={e => setNewThreadMessage(e.target.value)}
            rows={5}
            style={{
              width: '100%',
              padding: '0.75rem',
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid var(--border-glow)',
              borderRadius: '8px',
              color: 'white',
              fontFamily: 'inherit',
              marginBottom: '1rem',
              resize: 'vertical'
            }}
          />
          <button
            onClick={createThread}
            style={{
              padding: '0.75rem 1.5rem',
              background: 'linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple))',
              border: 'none',
              borderRadius: '8px',
              color: 'white',
              fontSize: '1rem',
              fontWeight: '600',
              cursor: 'pointer'
            }}
          >
            Créer le ticket
          </button>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: selectedThread ? '1fr 2fr' : '1fr', gap: '2rem' }}>
        {/* Threads List */}
        <div>
          <h2 style={{ marginBottom: '1rem', fontSize: '1.25rem' }}>Mes tickets</h2>
          {threads.length === 0 ? (
            <p style={{ color: 'var(--text-dim)' }}>Aucun ticket pour le moment</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {threads.map(thread => (
                <div
                  key={thread.id}
                  onClick={() => setSelectedThread(thread)}
                  style={{
                    padding: '1rem',
                    background: selectedThread?.id === thread.id ? 'rgba(139, 92, 246, 0.1)' : 'rgba(255,255,255,0.02)',
                    border: `1px solid ${selectedThread?.id === thread.id ? 'var(--galaxy-purple)' : 'var(--border-glow)'}`,
                    borderRadius: '8px',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <span style={{ fontWeight: '600' }}>{thread.subject}</span>
                    {thread.closed && (
                      <span style={{ 
                        fontSize: '0.75rem', 
                        padding: '0.25rem 0.5rem',
                        background: 'rgba(239, 68, 68, 0.2)',
                        color: '#ef4444',
                        borderRadius: '4px'
                      }}>
                        Fermé
                      </span>
                    )}
                  </div>
                  <p style={{ fontSize: '0.875rem', color: 'var(--text-dim)' }}>
                    {thread.messages.length} message{thread.messages.length > 1 ? 's' : ''}
                  </p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Thread Messages */}
        {selectedThread && (
          <div style={{
            background: 'rgba(255,255,255,0.02)',
            border: '1px solid var(--border-glow)',
            borderRadius: '12px',
            padding: '1.5rem',
            display: 'flex',
            flexDirection: 'column',
            maxHeight: '70vh'
          }}>
            <div style={{ marginBottom: '1rem', paddingBottom: '1rem', borderBottom: '1px solid var(--border-glow)' }}>
              <h2 style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>{selectedThread.subject}</h2>
              <p style={{ fontSize: '0.875rem', color: 'var(--text-dim)' }}>
                {new Date(selectedThread.created_at * 1000).toLocaleString('fr-FR')}
              </p>
            </div>

            {/* Messages */}
            <div style={{ flex: 1, overflowY: 'auto', marginBottom: '1rem', display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {selectedThread.messages.map(msg => (
                <div
                  key={msg.id}
                  style={{
                    padding: '1rem',
                    background: msg.author_user_id ? 'rgba(139, 92, 246, 0.1)' : 'rgba(34, 211, 238, 0.1)',
                    border: `1px solid ${msg.author_user_id ? 'var(--galaxy-purple)' : 'var(--galaxy-cyan)'}`,
                    borderRadius: '8px',
                    alignSelf: msg.author_user_id ? 'flex-end' : 'flex-start',
                    maxWidth: '80%'
                  }}
                >
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-dim)', marginBottom: '0.5rem' }}>
                    {msg.author_user_id ? 'Vous' : '🛡️ Support'} - {new Date(msg.created_at * 1000).toLocaleTimeString('fr-FR')}
                  </p>
                  <p style={{ whiteSpace: 'pre-wrap' }}>{msg.body}</p>
                </div>
              ))}
            </div>

            {/* New Message Input */}
            {!selectedThread.closed && (
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <textarea
                  placeholder="Votre message..."
                  value={newMessage}
                  onChange={e => setNewMessage(e.target.value)}
                  onKeyDown={e => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault()
                      sendMessage(selectedThread.id)
                    }
                  }}
                  rows={3}
                  style={{
                    flex: 1,
                    padding: '0.75rem',
                    background: 'rgba(255,255,255,0.05)',
                    border: '1px solid var(--border-glow)',
                    borderRadius: '8px',
                    color: 'white',
                    fontFamily: 'inherit',
                    resize: 'none'
                  }}
                />
                <button
                  onClick={() => sendMessage(selectedThread.id)}
                  style={{
                    padding: '0.75rem 1.5rem',
                    background: 'linear-gradient(135deg, var(--galaxy-cyan), var(--galaxy-purple))',
                    border: 'none',
                    borderRadius: '8px',
                    color: 'white',
                    fontSize: '1rem',
                    fontWeight: '600',
                    cursor: 'pointer',
                    alignSelf: 'flex-end'
                  }}
                >
                  Envoyer
                </button>
              </div>
            )}
            
            {selectedThread.closed && (
              <p style={{ 
                textAlign: 'center', 
                color: 'var(--text-dim)',
                padding: '1rem',
                background: 'rgba(239, 68, 68, 0.1)',
                borderRadius: '8px'
              }}>
                Ce ticket est fermé
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  )
}
