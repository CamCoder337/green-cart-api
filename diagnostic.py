#!/usr/bin/env python3
"""
Script de diagnostic rapide pour identifier les problèmes de déploiement.
"""
import os
import sys

def main():
    print("🔍 GreenCart Diagnostic")
    print("=" * 30)
    
    # Test des variables d'environnement critiques
    print("📋 Variables d'environnement:")
    critical_vars = ['DATABASE_URL', 'SECRET_KEY']
    optional_vars = ['ALLOWED_HOSTS', 'PORT', 'WORKERS']
    
    for var in critical_vars:
        value = os.environ.get(var)
        status = "✅" if value else "❌"
        print(f"{status} {var}: {'SET' if value else 'MISSING'}")
    
    for var in optional_vars:
        value = os.environ.get(var, 'DEFAULT')
        print(f"ℹ️  {var}: {value}")
    
    # Test d'import Django
    print("\n🐍 Test Django:")
    try:
        import django
        print(f"✅ Django version: {django.get_version()}")
        
        # Test des settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.production_minimal')
        django.setup()
        print("✅ Settings loaded successfully")
        
        # Test de la base de données
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Database connection OK")
        
    except Exception as e:
        print(f"❌ Django error: {e}")
        return False
    
    print("\n🎉 All checks passed!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)