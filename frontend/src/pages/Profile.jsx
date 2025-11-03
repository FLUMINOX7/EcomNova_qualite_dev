import React, { useEffect, useState } from 'react'
import { useAuth } from '../contexts/AuthContext'
import { getMe, updateMe } from '../utils/api'
import { useNotify } from '../contexts/NotificationContext'

const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/
const nameRegex = /^[A-Za-zÀ-ÖØ-öø-ÿ'\-\s]{2,}$/

export default function Profile() {
  const { isAuthenticated, user, login } = useAuth()
  const { show } = useNotify()

  const [form, setForm] = useState({
    email: '',
    first_name: '',
    last_name: '',
    address: ''
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    const load = async () => {
      try {
        const me = await getMe()
        setForm({
          email: me.email || '',
          first_name: me.first_name || '',
          last_name: me.last_name || '',
          address: me.address || ''
        })
      } catch (e) {
        show("Impossible de charger le profil", 'error')
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  const validate = (data) => {
    const errs = {}
    if (!emailRegex.test(data.email)) errs.email = 'Email invalide'
    if (!nameRegex.test(data.first_name)) errs.first_name = 'Prénom invalide (2+ lettres, apostrophe/trait d’union autorisés)'
    if (!nameRegex.test(data.last_name)) errs.last_name = 'Nom invalide (2+ lettres, apostrophe/trait d’union autorisés)'
    if (!data.address || data.address.trim().length < 5) errs.address = 'Adresse trop courte'
    return errs
  }

  const onChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    const errs = validate(form)
    setErrors(errs)
    if (Object.keys(errs).length) return

    setSaving(true)
    try {
      const updated = await updateMe(form)
      // refresh auth user in context
      login(updated, localStorage.getItem('token'))
      show('Profil mis à jour', 'success')
    } catch (e) {
      let msg = 'Mise à jour impossible'
      if (String(e).includes('Email already registered')) msg = 'Cet email est déjà utilisé'
      show(msg, 'error')
    } finally {
      setSaving(false)
    }
  }

  if (!isAuthenticated) {
    return <div className="error">Vous devez être connecté pour accéder au profil.</div>
  }
  if (loading) return <div className="loading">Chargement du profil…</div>

  return (
    <div style={{ maxWidth: 600, margin: '0 auto' }}>
      <h1 style={{ marginBottom: '1.5rem' }}>Mon profil</h1>
      <form onSubmit={onSubmit} style={{ display: 'grid', gap: '1rem' }}>
        <div>
          <label>Email</label>
          <input name="email" type="email" value={form.email} onChange={onChange} />
          {errors.email && <div className="error" style={{ marginTop: 6 }}>{errors.email}</div>}
        </div>
        <div>
          <label>Prénom</label>
          <input name="first_name" value={form.first_name} onChange={onChange} />
          {errors.first_name && <div className="error" style={{ marginTop: 6 }}>{errors.first_name}</div>}
        </div>
        <div>
          <label>Nom</label>
          <input name="last_name" value={form.last_name} onChange={onChange} />
          {errors.last_name && <div className="error" style={{ marginTop: 6 }}>{errors.last_name}</div>}
        </div>
        <div>
          <label>Adresse</label>
          <textarea name="address" rows={3} value={form.address} onChange={onChange} />
          {errors.address && <div className="error" style={{ marginTop: 6 }}>{errors.address}</div>}
        </div>
        <button className="btn" type="submit" disabled={saving}>{saving ? 'Enregistrement…' : 'Sauvegarder'}</button>
      </form>
    </div>
  )
}
