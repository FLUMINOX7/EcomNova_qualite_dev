import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Checkout from '../pages/Checkout'
import { AuthProvider } from '../contexts/AuthContext'
import { CartProvider } from '../contexts/CartContext'
import { NotificationProvider } from '../contexts/NotificationContext'

vi.mock('../utils/api', async () => {
  const actual = await vi.importActual('../utils/api')
  return {
    ...actual,
    createOrder: vi.fn().mockResolvedValue({ 
      id: 'o1',
      items: [
        { 
          id: 'item1', 
          product_id: 'p1', 
          name: 'Produit 1', 
          unit_price_cents: 1000, 
          quantity: 2,
          total_price_cents: 2000
        }
      ],
      total_price_cents: 2000
    })
  }
})

function setupAuthAndCart() {
  localStorage.setItem('token', 'test-token')
  localStorage.setItem('user', JSON.stringify({
    email: 'user@example.com',
    first_name: 'Jean',
    last_name: 'Dupont',
    address: '1 rue de la Paix\n75000 Paris'
  }))
  localStorage.setItem('cart', JSON.stringify({
    items: [
      { product: { id: 'p1', name: 'Produit 1', price_cents: 1000 }, quantity: 2 }
    ]
  }))
}

function renderCheckout() {
  return render(
    <MemoryRouter>
      <NotificationProvider>
        <AuthProvider>
          <CartProvider>
            <Checkout />
          </CartProvider>
        </AuthProvider>
      </NotificationProvider>
    </MemoryRouter>
  )
}

describe('Checkout (payment simulation)', () => {
  beforeEach(() => {
    localStorage.clear()
    setupAuthAndCart()
  })

  it('disables submit until card inputs are valid', () => {
    renderCheckout()
    const submit = screen.getByRole('button', { name: /Confirmer et payer/i })
    expect(submit).toBeDisabled()

    fireEvent.change(screen.getByLabelText(/Nom sur la carte/i), { target: { value: 'Jean Dupont' } })
    fireEvent.change(screen.getByLabelText(/Numéro de carte/i), { target: { value: '4242 4242 4242 4242' } })
    fireEvent.change(screen.getByLabelText(/Expiration/i), { target: { value: '12/29' } })
    fireEvent.change(screen.getByLabelText(/CVV/i), { target: { value: '123' } })

    expect(submit).not.toBeDisabled()
  })

  it('shows error for invalid card number', () => {
    renderCheckout()
    fireEvent.change(screen.getByLabelText(/Numéro de carte/i), { target: { value: '1234 5678 9012 3456' } })
    expect(screen.getByText(/Numéro de carte invalide/i)).toBeInTheDocument()
  })

  it('submits and shows success after valid inputs', async () => {
    const { createOrder } = await import('../utils/api')
    
    // Mock the payment endpoint
    global.fetch = vi.fn(() =>
      Promise.resolve({
        ok: true,
        json: () => Promise.resolve({ 
          id: 'payment123',
          succeeded: true 
        })
      })
    )

    renderCheckout()
    fireEvent.change(screen.getByLabelText(/Nom sur la carte/i), { target: { value: 'Jean Dupont' } })
    fireEvent.change(screen.getByLabelText(/Numéro de carte/i), { target: { value: '4242 4242 4242 4242' } })
    fireEvent.change(screen.getByLabelText(/Expiration/i), { target: { value: '12/29' } })
    fireEvent.change(screen.getByLabelText(/CVV/i), { target: { value: '123' } })

    fireEvent.click(screen.getByRole('button', { name: /Confirmer et payer/i }))

    await waitFor(() => {
      expect(createOrder).toHaveBeenCalled()
    })
    expect(screen.getByText(/Commande payée avec succès/i)).toBeInTheDocument()
  })
})
