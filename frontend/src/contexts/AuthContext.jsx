import React, { createContext, useContext, useState, useEffect } from 'react'
import { getMe } from '../utils/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Load token from localStorage on mount and verify it
    const savedToken = localStorage.getItem('token')
    const savedUser = localStorage.getItem('user')
    if (savedToken && savedUser) {
      setToken(savedToken)
      setUser(JSON.parse(savedUser))
      
      // Verify the token is still valid by fetching user data
      getMe()
        .then(userData => {
          // Update user data from server
          setUser(userData)
          localStorage.setItem('user', JSON.stringify(userData))
        })
        .catch(err => {
          // Token invalid or user doesn't exist anymore
          if (err.isAuthError || err.status === 401) {
            // Clear invalid session
            setUser(null)
            setToken(null)
            localStorage.removeItem('token')
            localStorage.removeItem('user')
          }
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = (userData, authToken) => {
    setUser(userData)
    setToken(authToken)
    localStorage.setItem('token', authToken)
    localStorage.setItem('user', JSON.stringify(userData))
  }

  const logout = () => {
    setUser(null)
    setToken(null)
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const value = {
    user,
    token,
    loading,
    isAuthenticated: !!token,
    login,
    logout
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
