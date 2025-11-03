import React from 'react'
import { useParams } from 'react-router-dom'

export default function Product() {
  const { id } = useParams()
  return (
    <div>
      <h2>Produit #{id}</h2>
      <p>Détails du produit (à implémenter)</p>
    </div>
  )
}
