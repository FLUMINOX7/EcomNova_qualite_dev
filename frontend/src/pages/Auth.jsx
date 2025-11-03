import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { login as apiLogin, register as apiRegister } from '../utils/api'
import { useNotify } from '../contexts/NotificationContext'

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
  const [fieldErrors, setFieldErrors] = useState({})

  const { login } = useAuth()
  const { show } = useNotify()
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }))
  }

  const validateRegister = (data) => {
    const errors = {}
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i
    // 8-72 chars, at least one letter and one digit
    const passwordRegex = /^(?=.*[A-Za-z])(?=.*\d).{8,72}$/
    const nameRegex = /^[A-Za-zÀ-ÖØ-öø-ÿ' -]{2,}$/

    if (!emailRegex.test(data.email)) {
      errors.email = 'Email invalide'
    }
    if (!passwordRegex.test(data.password)) {
      errors.password = '8-72 caractères, au moins 1 lettre et 1 chiffre'
    }
    if (!nameRegex.test(data.firstName)) {
      errors.firstName = 'Prénom invalide (2+ lettres, accents autorisés)'
    }
    if (!nameRegex.test(data.lastName)) {
      errors.lastName = 'Nom invalide (2+ lettres, accents autorisés)'
    }
    if (!data.address || data.address.trim().length < 5) {
      errors.address = "Adresse trop courte"
    }
    return errors
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setFieldErrors({})

    if (mode === 'register') {
      const errors = validateRegister(formData)
      if (Object.keys(errors).length > 0) {
        setFieldErrors(errors)
        show('Veuillez corriger les erreurs du formulaire', 'error')
        return
      }
    }

    setLoading(true)
    try {
      if (mode === 'login') {
        const data = await apiLogin(formData.email, formData.password)
        login(data.user, data.access_token)
        show('Connexion réussie', 'success')
        navigate('/')
      } else {
        const data = await apiRegister(
          formData.email,
          formData.password,
          formData.firstName,
          formData.lastName,
          formData.address
        )
        login(data.user, data.access_token)
        show('Inscription réussie', 'success')
        navigate('/')
      }
    } catch (err) {
      const msg = err?.message || 'Une erreur est survenue'
      setError(msg)
      show(msg, 'error')
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
          {mode === 'register' && fieldErrors.email && (
            <div className="error" style={{ marginTop: 6 }}>{fieldErrors.email}</div>
          )}
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
          {mode === 'register' && fieldErrors.password && (
            <div className="error" style={{ marginTop: 6 }}>{fieldErrors.password}</div>
          )}
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
              {fieldErrors.firstName && (
                <div className="error" style={{ marginTop: 6 }}>{fieldErrors.firstName}</div>
              )}
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
              {fieldErrors.lastName && (
                <div className="error" style={{ marginTop: 6 }}>{fieldErrors.lastName}</div>
              )}
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
              {fieldErrors.address && (
                <div className="error" style={{ marginTop: 6 }}>{fieldErrors.address}</div>
              )}
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
            setFieldErrors({})
          }}
          style={{
            background: 'none',
            border: 'none',
            color: 'var(--galaxy-cyan)',
            cursor: 'pointer',
            textDecoration: 'underline',
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

