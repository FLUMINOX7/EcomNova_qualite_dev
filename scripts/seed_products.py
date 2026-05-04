"""
Seed data script for EcomNova - Adds demo products to the database
"""

import uuid

from sqlalchemy.orm import Session

from backend.dependencies import get_session
from backend.models_sql import ProductModel

DEMO_PRODUCTS = [
    {
        "name": "QuantumCore X1 Processor",
        "description": "Processeur quantique nouvelle génération avec 512 qubits. Performance révolutionnaire pour le calcul parallèle et l'IA avancée.",
        "price": 2499.99,
        "stock": 15,
        "category": "Computing",
        "image": "https://images.unsplash.com/photo-1555617981-dac3880eac6e?w=400",
    },
    {
        "name": "NovaSphere VR Headset",
        "description": "Casque de réalité virtuelle immersive avec résolution 8K par œil, tracking neural et champ de vision 210°.",
        "price": 1899.99,
        "stock": 25,
        "category": "VR",
        "image": "https://images.unsplash.com/photo-1617802690992-15d93263d3a9?w=400",
    },
    {
        "name": "HyperLink Neural Interface",
        "description": "Interface cerveau-machine non invasive permettant le contrôle mental d'appareils connectés. Technologie de pointe approuvée.",
        "price": 3999.99,
        "stock": 8,
        "category": "Neural Tech",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
    },
    {
        "name": "StarDrive Holographic Display",
        "description": "Écran holographique 3D autonome de 65 pouces. Projection volumétrique sans lunettes, parfait pour la collaboration.",
        "price": 4599.99,
        "stock": 12,
        "category": "Displays",
        "image": "https://images.unsplash.com/photo-1593640408182-31c70c8268f5?w=400",
    },
    {
        "name": "AeroGlide Smart Drone Pro",
        "description": "Drone autonome avec IA embarquée, vol silencieux, autonomie 2h, caméra 6K stabilisée et mode suivi intelligent.",
        "price": 1299.99,
        "stock": 30,
        "category": "Drones",
        "image": "https://images.unsplash.com/photo-1473968512647-3e447244af8f?w=400",
    },
    {
        "name": "CyberShield Security Suite",
        "description": "Suite de sécurité quantique avec chiffrement post-quantique, protection temps réel et pare-feu neuronal adaptatif.",
        "price": 799.99,
        "stock": 50,
        "category": "Security",
        "image": "https://images.unsplash.com/photo-1563206767-5b18f218e8de?w=400",
    },
    {
        "name": "NanoBot Medical Scanner",
        "description": "Scanner médical portable utilisant des nanobots pour diagnostic précis en 30 secondes. Usage personnel certifié.",
        "price": 5499.99,
        "stock": 5,
        "category": "Medical",
        "image": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=400",
    },
    {
        "name": "FusionCell Power Station",
        "description": "Station d'énergie à fusion froide compacte, 10kW continus, autonomie 20 ans, zéro émission, révolution énergétique.",
        "price": 8999.99,
        "stock": 3,
        "category": "Energy",
        "image": "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=400",
    },
    {
        "name": "GravityWave Audio System",
        "description": "Système audio à ondes gravitationnelles. Son 360° sans enceintes visibles, qualité studio, technologie spatiale.",
        "price": 2199.99,
        "stock": 20,
        "category": "Audio",
        "image": "https://images.unsplash.com/photo-1545127398-14699f92334b?w=400",
    },
    {
        "name": "TelePort Data Hub",
        "description": "Hub de transfert de données instantané par téléportation quantique. 10 Pb/s, latence 0ms, portée 1000km.",
        "price": 6799.99,
        "stock": 7,
        "category": "Networking",
        "image": "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=400",
    },
    {
        "name": "BioSync Fitness Tracker",
        "description": "Tracker fitness bio-intégré avec surveillance ADN, prédiction maladies, coaching IA personnalisé 24/7.",
        "price": 899.99,
        "stock": 40,
        "category": "Health",
        "image": "https://images.unsplash.com/photo-1516574187841-cb9cc2ca948b?w=400",
    },
    {
        "name": "EchoMind AI Assistant",
        "description": "Assistant IA conscient avec personnalité évolutive. Gestion complète de votre vie numérique et physique.",
        "price": 3299.99,
        "stock": 18,
        "category": "AI",
        "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400",
    },
    {
        "name": "PhotonBeam Laser Projector",
        "description": "Projecteur laser 4K ultra-courte focale avec correction automatique et projection jusqu'à 300 pouces.",
        "price": 1799.99,
        "stock": 22,
        "category": "Displays",
        "image": "https://images.unsplash.com/photo-1593784991095-a205069470b6?w=400",
    },
    {
        "name": "SkyGuard Security Drone",
        "description": "Drone de surveillance autonome avec détection IA, vision nocturne et patrouille programmable 24/7.",
        "price": 2499.99,
        "stock": 14,
        "category": "Drones",
        "image": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=400",
    },
    {
        "name": "MindSync Sleep Optimizer",
        "description": "Système d'optimisation du sommeil avec ondes cérébrales, aromathérapie intelligente et réveil progressif.",
        "price": 699.99,
        "stock": 35,
        "category": "Health",
        "image": "https://images.unsplash.com/photo-1541480551145-2370a440d585?w=400",
    },
    {
        "name": "HyperCore Gaming Rig",
        "description": "PC gaming ultra-puissant avec RTX 5090, refroidissement liquide et RGB synchronisé. Prêt pour le gaming 8K.",
        "price": 4299.99,
        "stock": 9,
        "category": "Computing",
        "image": "https://images.unsplash.com/photo-1587202372634-32705e3bf49c?w=400",
    },
    {
        "name": "SmartFabric Wearable Tech",
        "description": "Vêtement intelligent avec capteurs biométriques intégrés, thermorégulation et connectivité sans fil.",
        "price": 449.99,
        "stock": 50,
        "category": "Health",
        "image": "https://images.unsplash.com/photo-1556906781-9a412961c28c?w=400",
    },
    {
        "name": "QuantumShield VPN Router",
        "description": "Routeur VPN quantique avec chiffrement inviolable, pare-feu IA et débit 10 Gbps.",
        "price": 899.99,
        "stock": 28,
        "category": "Networking",
        "image": "https://images.unsplash.com/photo-1606904825846-647eb07f5be2?w=400",
    },
    {
        "name": "AirPure Nano Purifier",
        "description": "Purificateur d'air à nanofiltration éliminant 99.99% virus, bactéries et particules. Silencieux et intelligent.",
        "price": 549.99,
        "stock": 42,
        "category": "Health",
        "image": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=400",
    },
    {
        "name": "NeuralLink Keyboard Pro",
        "description": "Clavier avec interface neuronale optionnelle, touches mécaniques personnalisables et apprentissage de frappe IA.",
        "price": 349.99,
        "stock": 60,
        "category": "Neural Tech",
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400",
    },
    {
        "name": "InfinityCharge Power Bank",
        "description": "Batterie externe solaire 50000mAh avec charge rapide 100W, ports multiples et écran OLED.",
        "price": 199.99,
        "stock": 80,
        "category": "Energy",
        "image": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400",
    },
    {
        "name": "CrystalSound ANC Headphones",
        "description": "Casque audio avec réduction de bruit active adaptative, son spatial 3D et autonomie 60h.",
        "price": 499.99,
        "stock": 45,
        "category": "Audio",
        "image": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=400",
    },
    {
        "name": "VisionPro AR Glasses",
        "description": "Lunettes de réalité augmentée légères avec affichage rétinien, commande vocale et traduction en temps réel.",
        "price": 2799.99,
        "stock": 16,
        "category": "VR",
        "image": "https://images.unsplash.com/photo-1617953141905-b27fb1f17d88?w=400",
    },
    {
        "name": "SecureVault Biometric Safe",
        "description": "Coffre-fort biométrique avec reconnaissance faciale, empreinte digitale et alerte intrusion instantanée.",
        "price": 1299.99,
        "stock": 12,
        "category": "Security",
        "image": "https://images.unsplash.com/photo-1565372195458-9de0b320ef04?w=400",
    },
    {
        "name": "SmartDesk Pro Workstation",
        "description": "Bureau intelligent à hauteur variable avec chargement sans fil, monitoring posture et éclairage adaptatif.",
        "price": 1599.99,
        "stock": 8,
        "category": "Other",
        "image": "https://images.unsplash.com/photo-1595515106969-1ce29566ff1c?w=400",
    },
    {
        "name": "HyperLoop Mini Transport",
        "description": "Système de transport personnel à lévitation magnétique pour déplacements urbains rapides et silencieux.",
        "price": 8499.99,
        "stock": 4,
        "category": "Other",
        "image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400",
    },
    {
        "name": "OxygenBoost Portable Generator",
        "description": "Générateur d'oxygène portable médical avec concentrateur à 95%, batterie 8h et mode silencieux.",
        "price": 1899.99,
        "stock": 11,
        "category": "Medical",
        "image": "https://images.unsplash.com/photo-1584982751601-97dcc096659c?w=400",
    },
    {
        "name": "FlexScreen Foldable Monitor",
        "description": "Écran pliable 27 pouces OLED 4K, ultra-fin, se roule dans son boîtier. Parfait pour nomades digitaux.",
        "price": 1999.99,
        "stock": 19,
        "category": "Displays",
        "image": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400",
    },
    {
        "name": "NanoClean Self-Cleaning Robot",
        "description": "Robot aspirateur-laveur avec stérilisation UV, mapping 3D et vidange automatique. 90 jours d'autonomie.",
        "price": 799.99,
        "stock": 33,
        "category": "AI",
        "image": "https://images.unsplash.com/photo-1563207153-f403bf289096?w=400",
    },
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
                existing.image_url = product_data.get("image") or product_data.get(
                    "image_url"
                )
                existing.price_cents = int(product_data["price"] * 100)
                existing.stock_qty = product_data["stock"]
                existing.active = True
                updated += 1
            else:
                product = ProductModel(
                    id=str(uuid.uuid4()),
                    name=product_data["name"],
                    description=product_data.get("description"),
                    image_url=product_data.get("image")
                    or product_data.get("image_url"),
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
            has_img = bool(p.get("image") or p.get("image_url"))
            print(f"  - {p['name']} - {p['price']}€ - {'🖼️' if has_img else '—'}")

    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed_products()
