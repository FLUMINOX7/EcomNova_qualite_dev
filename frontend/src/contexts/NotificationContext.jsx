import React, { createContext, useContext, useState, useCallback } from 'react'

const NotificationContext = createContext(null)

export function NotificationProvider({ children }) {
  const [message, setMessage] = useState(null)
  const [type, setType] = useState('info') // 'success' | 'error' | 'info'

  const show = useCallback((msg, kind = 'info', timeout = 3000) => {
    setMessage(msg)
    setType(kind)
    if (timeout) {
      setTimeout(() => setMessage(null), timeout)
    }
  }, [])

  return (
    <NotificationContext.Provider value={{ show }}>
      {message && (
        <div
          style={{
            position: 'fixed', top: 0, left: 0, right: 0,
            padding: '12px 16px',
            textAlign: 'center',
            zIndex: 200,
            background: type === 'success' ? 'rgba(34,197,94,0.2)' : type === 'error' ? 'rgba(239,68,68,0.2)' : 'rgba(59,130,246,0.2)',
            borderBottom: '1px solid var(--border-glow)',
            backdropFilter: 'blur(8px)'
          }}
        >
          <span style={{ color: type === 'success' ? '#86efac' : type === 'error' ? '#fca5a5' : 'var(--galaxy-cyan)' }}>{message}</span>
        </div>
      )}
      {children}
    </NotificationContext.Provider>
  )
}

export function useNotify() {
  const ctx = useContext(NotificationContext)
  if (!ctx) throw new Error('useNotify must be used within NotificationProvider')
  return ctx
}
