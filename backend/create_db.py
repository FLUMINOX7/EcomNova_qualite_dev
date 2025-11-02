#!/usr/bin/env python3
"""
Script pour créer automatiquement toutes les tables dans la base de données
en utilisant les modèles SQLAlchemy.

Usage:
    python backend/create_db.py
    
    Ou avec des variables d'environnement:
    export DATABASE_URL="postgresql://user:password@localhost:5432/dbname"
    python backend/create_db.py
"""

import os
import sys
from sqlalchemy import create_engine, text
from models_sql import Base

def get_database_url():
    """Récupère l'URL de la base de données"""
    
    # 1. Essayer depuis les variables d'environnement
    if "DATABASE_URL" in os.environ:
        return os.environ["DATABASE_URL"]
    
    # 2. Essayer de charger depuis un fichier .env
    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        print(f"📁 Chargement des variables depuis {env_file}")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    if key.strip() == "DATABASE_URL":
                        return value.strip().strip('"').strip("'")
    
    # 3. Demander interactivement
    print("\n⚠️  Variable DATABASE_URL non trouvée")
    print("\n💡 Format attendu: postgresql://user:password@host:port/database")
    print("\nExemple: postgresql://ecomnova_user:password@localhost:5432/ecomnova")
    
    database_url = input("\nEntrez l'URL de connexion PostgreSQL: ").strip()
    if not database_url:
        print("❌ URL vide, abandon.")
        sys.exit(1)
    
    return database_url

def test_connection(engine):
    """Teste la connexion à la base de données"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"\n❌ Erreur de connexion: {e}")
        return False

def create_tables():
    """Crée toutes les tables définies dans les modèles SQLAlchemy"""
    
    database_url = get_database_url()
    
    # Masquer le mot de passe dans l'affichage
    display_url = database_url
    if "@" in database_url and ":" in database_url.split("@")[0]:
        parts = database_url.split("@")
        user_pass = parts[0].split("//")[1]
        if ":" in user_pass:
            user, password = user_pass.split(":", 1)
            display_url = database_url.replace(f":{password}@", ":***@")
    
    print(f"\n🔄 Connexion à la base de données...")
    print(f"   URL: {display_url}")
    
    # Créer le moteur de base de données
    try:
        engine = create_engine(database_url)
    except Exception as e:
        print(f"\n❌ Erreur lors de la création du moteur: {e}")
        sys.exit(1)
    
    # Tester la connexion
    print("\n🔍 Test de connexion...")
    if not test_connection(engine):
        print("\n💡 Vérifiez:")
        print("   - Que PostgreSQL est démarré")
        print("   - Que l'utilisateur et le mot de passe sont corrects")
        print("   - Que la base de données existe")
        sys.exit(1)
    
    print("✅ Connexion réussie!")
    
    print("\n🔄 Création des tables...")
    
    try:
        # Créer toutes les tables
        Base.metadata.create_all(bind=engine)
        
        print("\n✅ Toutes les tables ont été créées avec succès!")
        print("\nTables créées:")
        for table_name in Base.metadata.tables.keys():
            print(f"  ✓ {table_name}")
    except Exception as e:
        print(f"\n❌ Erreur lors de la création des tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_tables()
