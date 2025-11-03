import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { login as apiLogin, register as apiRegister } from '../utils/api'

export default function Auth() {
  const [mode, setMode] = useState('login') // 'login' or 'register'
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    firstName: '',
    lastName: '',
    address: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      if (mode === 'login') {
        const data = await apiLogin(formData.email, formData.password)
        login({ email: formData.email, id: data.user_id }, data.token)
        navigate('/')
      } else {
        const data = await apiRegister(
          formData.email,
          formData.password,
          formData.firstName,
          formData.lastName,
          formData.address
        )
        login({ email: formData.email, id: data.user_id }, data.token)
        navigate('/')
      }
    } catch (err) {
      setError(err.message || 'Une erreur est survenue')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ maxWidth: '500px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '2rem', textAlign: 'center' }}>
        {mode === 'login' ? 'Connexion' : 'Inscription'}
      </h1>

      {error && <div className="error">{error}</div>}

      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            placeholder="votre@email.com"
          />
        </div>

        <div>
          <label style={{ display: 'block', marginBottom: '0.5rem' }}>Mot de passe</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            placeholder="••••••••"
          />
        </div>

        {mode === 'register' && (
          <>
            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Prénom</label>
              <input
                type="text"
                name="firstName"
                value={formData.firstName}
                onChange={handleChange}
                required
                placeholder="John"
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Nom</label>
              <input
                type="text"
                name="lastName"
                value={formData.lastName}
                onChange={handleChange}
                required
                placeholder="Doe"
              />
            </div>

            <div>
              <label style={{ display: 'block', marginBottom: '0.5rem' }}>Adresse</label>
              <textarea
                name="address"
                value={formData.address}
                onChange={handleChange}
                required
                placeholder="123 Rue de la Technologie, 75001 Paris"
                rows="3"
              />
            </div>
          </>
        )}

        <button type="submit" className="btn" disabled={loading} style={{ marginTop: '1rem' }}>
          {loading ? 'Chargement...' : (mode === 'login' ? 'Se connecter' : "S'inscrire")}
        </button>
      </form>

      <div style={{ textAlign: 'center', marginTop: '1.5rem' }}>
        <button
          onClick={() => {
            setMode(mode === 'login' ? 'register' : 'login')
            setError('')
          }}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--galaxy-cyan)',
            cursor: 'pointer',
            textDecoration: 'underline'
          }}
        >
          {mode === 'login'
            ? "Pas encore de compte ? S'inscrire"
            : 'Déjà un compte ? Se connecter'}
        </button>
      </div>
    </div>
  )
}

