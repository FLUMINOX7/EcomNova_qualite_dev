#!/usr/bin/env python3
"""
Script pour ajouter des produits au catalogue EcomNova.

Usage:
    python scripts/add_products.py

Ce script ajoute des produits via l'API REST avec authentification admin.
"""

import requests
import json
import sys
import os

# URL de base de l'API (à ajuster selon votre configuration)
BASE_URL = "http://localhost:8000/api/v1"

# Identifiants admin par défaut
ADMIN_EMAIL = "admin@shop.test"
ADMIN_PASSWORD = "admin"

def authenticate():
    """Authentifie l'utilisateur admin et retourne le token."""
    try:
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
        )
        response.raise_for_status()
        return response.json()["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur d'authentification: {e}")
        print("💡 Vérifiez que l'API est démarrée et que les identifiants sont corrects")
        sys.exit(1)

def create_product(token, product_data):
    """Crée un produit via l'API."""
    try:
        response = requests.post(
            f"{BASE_URL}/products",
            json=product_data,
            headers={"Authorization": f"Bearer {token}"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la création du produit '{product_data['name']}': {e}")
        return None

def main():
    """Fonction principale du script."""
    print("🛒 Script d'ajout de produits EcomNova")
    print("=" * 50)
    
    # Authentification
    print("🔐 Authentification admin...")
    token = authenticate()
    print("✅ Authentification réussie!")
    
    # Produits à ajouter
    products = [
        {
            "name": "T-Shirt Classique Blanc",
            "description": "T-shirt en coton bio 100%, coupe classique, disponible en plusieurs tailles",
            "image_url": "https://example.com/images/tshirt-blanc.jpg",
            "price_cents": 1999,  # 19.99€
            "stock_qty": 50,
            "active": True
        },
        {
            "name": "Sweat à Capuche Premium",
            "description": "Sweat-shirt en molleton premium avec capuche, très confortable",
            "image_url": "https://example.com/images/sweat-capuche.jpg",
            "price_cents": 4999,  # 49.99€
            "stock_qty": 25,
            "active": True
        },
        {
            "name": "Jean Slim Bleu",
            "description": "Jean slim en denim stretch, coupe moderne et confortable",
            "image_url": "https://example.com/images/jean-slim.jpg",
            "price_cents": 6999,  # 69.99€
            "stock_qty": 30,
            "active": True
        },
        {
            "name": "Basket Sportive",
            "description": "Chaussures de sport légères et respirantes, idéales pour le quotidien",
            "image_url": "https://example.com/images/basket-sport.jpg",
            "price_cents": 8999,  # 89.99€
            "stock_qty": 20,
            "active": True
        },
        {
            "name": "Veste en Cuir",
            "description": "Veste en cuir véritable, style intemporel et élégant",
            "image_url": "https://example.com/images/veste-cuir.jpg",
            "price_cents": 19999,  # 199.99€
            "stock_qty": 10,
            "active": True
        }
    ]
    
    # Création des produits
    print(f"\n📦 Ajout de {len(products)} produits...")
    created_count = 0
    
    for product_data in products:
        print(f"\n⏳ Création de '{product_data['name']}'...")
        result = create_product(token, product_data)
        
        if result:
            print(f"✅ Produit créé avec succès (ID: {result['id']})")
            print(f"   Prix: {result['price_cents']/100:.2f}€")
            print(f"   Stock: {result['stock_qty']} unités")
            created_count += 1
        else:
            print(f"❌ Échec de la création")
    
    # Résumé
    print("\n" + "=" * 50)
    print(f"📊 Résumé: {created_count}/{len(products)} produits créés avec succès")
    
    if created_count > 0:
        print("🎉 Produits ajoutés au catalogue!")
        print("💡 Vous pouvez maintenant les voir sur l'interface web")
    else:
        print("⚠️  Aucun produit n'a été créé")

if __name__ == "__main__":
    main()