import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Auth from '../pages/Auth'
import { AuthProvider } from '../contexts/AuthContext'
import { NotificationProvider } from '../contexts/NotificationContext'

describe('Auth page', () => {
  it('shows login title by default', () => {
    render(
      <MemoryRouter>
        <NotificationProvider>
          <AuthProvider>
            <Auth />
          </AuthProvider>
        </NotificationProvider>
      </MemoryRouter>
    )
    expect(screen.getByText(/Connexion/)).toBeInTheDocument()
  })
})
