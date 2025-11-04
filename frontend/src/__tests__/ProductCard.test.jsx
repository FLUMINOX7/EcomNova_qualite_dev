import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import ProductCard from '../components/ProductCard'
import { CartProvider } from '../contexts/CartContext'
import { AuthProvider } from '../contexts/AuthContext'
import { NotificationProvider } from '../contexts/NotificationContext'

const sample = {
  id: 'p1',
  name: 'QuantumCore X1',
  description: 'Processeur quantique',
  price_cents: 249999,
}

describe('ProductCard', () => {
  it('renders name and price', () => {
    render(
      <MemoryRouter>
        <NotificationProvider>
          <AuthProvider>
            <CartProvider>
              <ProductCard product={sample} />
            </CartProvider>
          </AuthProvider>
        </NotificationProvider>
      </MemoryRouter>
    )
    expect(screen.getByText(/QuantumCore X1/)).toBeInTheDocument()
    expect(screen.getByText(/2499.99 €/)).toBeInTheDocument()
  })
})
