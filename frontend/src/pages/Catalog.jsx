import React from 'react'
import { Navigate } from 'react-router-dom'

// Redirect to new Products page for backward compatibility
export default function Catalog() {
  return <Navigate to="/products" replace />
}
