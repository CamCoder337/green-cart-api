#!/usr/bin/env python
"""
Script pour ajouter un endpoint de login dans Swagger
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
django.setup()

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token

def test_login_endpoint():
    """Affiche les tokens existants."""
    User = get_user_model()
    
    print("🔑 Tokens disponibles pour l'authentification Swagger:\n")
    
    # Récupère les tokens existants
    users_with_tokens = User.objects.filter(auth_token__isnull=False)
    
    for user in users_with_tokens:
        print(f"📧 {user.email}")
        print(f"🔑 Token: {user.auth_token.key}")
        print(f"👤 Type: {user.get_user_type_display()}")
        print("-" * 50)
    
    print("📋 Comptes de test disponibles:")
    print("Consumer: consumer@test.com / testpass123") 
    print("Producer 1: ferme.bio@test.com / testpass123")
    print("Producer 2: maraicher.local@test.com / testpass123")
    
    print(f"\n🌐 Accédez à Swagger: http://127.0.0.1:8000/api/docs/")
    print("1. Cliquez sur 'Authorize' en haut à droite")
    print("2. Entrez le token avec le format: Token votre_token_ici")
    print("3. Vous serez authentifié pour tous les endpoints!")
    print("\n💡 Conseil: Pour obtenir un token, faites d'abord un POST /api/auth/login/ avec email/password")

if __name__ == '__main__':
    test_login_endpoint()