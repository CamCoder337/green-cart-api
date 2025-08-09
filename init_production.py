#!/usr/bin/env python3
"""
Script d'initialisation pour l'environnement de production.
Vérifie les variables d'environnement requises.
"""
import os
import sys

def check_environment():
    """Vérifie les variables d'environnement critiques."""
    
    required_vars = {
        'DATABASE_URL': 'URL de la base de données PostgreSQL',
        'SECRET_KEY': 'Clé secrète Django (générée automatiquement par Render)',
    }
    
    optional_vars = {
        'ALLOWED_HOSTS': '*',
        'CORS_ALLOWED_ORIGINS': 'https://*.onrender.com,http://localhost:3000',
        'PORT': '8000',
        'WORKERS': '3',
        'POPULATE_TEST_DATA': 'true',
    }
    
    print("🔍 Vérification des variables d'environnement...")
    print("=" * 50)
    
    missing_required = []
    
    # Vérifier les variables requises
    for var, description in required_vars.items():
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {'*' * min(len(value), 20)}...")
        else:
            print(f"❌ {var}: MANQUANT - {description}")
            missing_required.append(var)
    
    # Afficher les variables optionnelles
    print("\n📋 Variables optionnelles:")
    for var, default in optional_vars.items():
        value = os.environ.get(var, default)
        print(f"ℹ️  {var}: {value}")
    
    if missing_required:
        print(f"\n💥 Erreur: Variables manquantes: {', '.join(missing_required)}")
        print("\n📚 Consultez RENDER_CONFIG.md pour la configuration complète")
        return False
    
    print("\n🎉 Configuration d'environnement OK!")
    return True

if __name__ == "__main__":
    success = check_environment()
    sys.exit(0 if success else 1)