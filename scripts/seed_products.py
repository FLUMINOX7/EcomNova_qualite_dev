"""
Seed data script for EcomNova - Adds demo products to the database
"""
import uuid
from backend.dependencies import get_session
from backend.models_sql import ProductModel
from sqlalchemy.orm import Session

DEMO_PRODUCTS = [
    {
        "name": "QuantumCore X1 Processor",
        "description": "Processeur quantique nouvelle génération avec 512 qubits. Performance révolutionnaire pour le calcul parallèle et l'IA avancée.",
        "price": 2499.99,
        "stock": 15,
        "category": "Computing",
        "image": "https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=400"
    },
    {
        "name": "NovaSphere VR Headset",
        "description": "Casque de réalité virtuelle immersive avec résolution 8K par œil, tracking neural et champ de vision 210°.",
        "price": 1899.99,
        "stock": 25,
        "category": "VR",
        "image": "https://images.unsplash.com/photo-1617802690992-15d93263d3a9?w=400"
    },
    {
        "name": "HyperLink Neural Interface",
        "description": "Interface cerveau-machine non invasive permettant le contrôle mental d'appareils connectés. Technologie de pointe approuvée.",
        "price": 3999.99,
        "stock": 8,
        "category": "Neural Tech",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400"
    },
    {
        "name": "StarDrive Holographic Display",
        "description": "Écran holographique 3D autonome de 65 pouces. Projection volumétrique sans lunettes, parfait pour la collaboration.",
        "price": 4599.99,
        "stock": 12,
        "category": "Displays",
        "image": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=400"
    },
    {
        "name": "AeroGlide Smart Drone Pro",
        "description": "Drone autonome avec IA embarquée, vol silencieux, autonomie 2h, caméra 6K stabilisée et mode suivi intelligent.",
        "price": 1299.99,
        "stock": 30,
        "category": "Drones",
        "image": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400"
    },
    {
        "name": "CyberShield Security Suite",
        "description": "Suite de sécurité quantique avec chiffrement post-quantique, protection temps réel et pare-feu neuronal adaptatif.",
        "price": 799.99,
        "stock": 50,
        "category": "Security",
        "image": "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=400"
    },
    {
        "name": "NanoBot Medical Scanner",
        "description": "Scanner médical portable utilisant des nanobots pour diagnostic précis en 30 secondes. Usage personnel certifié.",
        "price": 5499.99,
        "stock": 5,
        "category": "Medical",
        "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400"
    },
    {
        "name": "FusionCell Power Station",
        "description": "Station d'énergie à fusion froide compacte, 10kW continus, autonomie 20 ans, zéro émission, révolution énergétique.",
        "price": 8999.99,
        "stock": 3,
        "category": "Energy",
        "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=400"
    },
    {
        "name": "GravityWave Audio System",
        "description": "Système audio à ondes gravitationnelles. Son 360° sans enceintes visibles, qualité studio, technologie spatiale.",
        "price": 2199.99,
        "stock": 20,
        "category": "Audio",
        "image": "https://images.unsplash.com/photo-1545127398-14699f92334b?w=400"
    },
    {
        "name": "TelePort Data Hub",
        "description": "Hub de transfert de données instantané par téléportation quantique. 10 Pb/s, latence 0ms, portée 1000km.",
        "price": 6799.99,
        "stock": 7,
        "category": "Networking",
        "image": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400"
    },
    {
        "name": "BioSync Fitness Tracker",
        "description": "Tracker fitness bio-intégré avec surveillance ADN, prédiction maladies, coaching IA personnalisé 24/7.",
        "price": 899.99,
        "stock": 40,
        "category": "Health",
        "image": "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=400"
    },
    {
        "name": "EchoMind AI Assistant",
        "description": "Assistant IA conscient avec personnalité évolutive. Gestion complète de votre vie numérique et physique.",
        "price": 3299.99,
        "stock": 18,
        "category": "AI",
        "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400"
    }
]


def seed_products():
    """Add demo products to the database"""
    session: Session = next(get_session())
    
    try:
        created = 0
        updated = 0

        # Upsert-like behavior by name: update existing, create missing
        for product_data in DEMO_PRODUCTS:
            existing = (
                session.query(ProductModel)
                .filter(ProductModel.name == product_data["name"])
                .first()
            )
            if existing:
                # Update fields (including backfilling image_url)
                existing.description = product_data.get("description")
                existing.image_url = product_data.get("image") or product_data.get("image_url")
                existing.price_cents = int(product_data["price"] * 100)
                existing.stock_qty = product_data["stock"]
                existing.active = True
                updated += 1
            else:
                product = ProductModel(
                    id=str(uuid.uuid4()),
                    name=product_data["name"],
                    description=product_data.get("description"),
                    image_url=product_data.get("image") or product_data.get("image_url"),
                    price_cents=int(product_data["price"] * 100),  # Convert to cents
                    stock_qty=product_data["stock"],
                    active=True,
                )
                session.add(product)
                created += 1

        session.commit()
        if created or updated:
            print(f"✓ Seed complete. Created: {created}, Updated: {updated}")
        else:
            print("✓ Seed checked. No changes needed (already up to date).")
        
        # Display summary of demo products with images
        print("\nDemo products (name — price — has image):")
        for p in DEMO_PRODUCTS:
            has_img = bool(p.get('image') or p.get('image_url'))
            print(f"  - {p['name']} - {p['price']}€ - {'🖼️' if has_img else '—'}")
    
    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_products()
