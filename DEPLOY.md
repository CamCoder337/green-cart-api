# Déploiement GreenCart API sur Render

## Configuration automatique

Le projet est configuré pour un déploiement automatique sur Render avec le fichier `render.yaml`.

### Étapes de déploiement :

1. **Fork ou push du repository** sur GitHub
2. **Connecter le repository** à votre compte Render
3. Le déploiement se fera automatiquement avec :
   - Base de données PostgreSQL
   - Web service avec Dockerfile
   - Variables d'environnement préconfigurées

### Fonctionnalités incluses au déploiement :

✅ **Superadmin par défaut** :
- Username: `admin`
- Email: `admin@greencart.com`
- Password: `admin123`

✅ **Données de test** automatiquement créées :
- Utilisateurs de test (consommateurs et producteurs)
- Catégories de produits
- Produits d'exemple
- Commandes de test

✅ **Tokens d'authentification** générés automatiquement

## Variables d'environnement

Les variables suivantes sont configurées automatiquement dans `render.yaml` :

| Variable | Valeur | Description |
|----------|---------|-------------|
| `DJANGO_SETTINGS_MODULE` | `core.settings.production` | Configuration production |
| `DEBUG` | `false` | Mode debug désactivé |
| `SECRET_KEY` | Auto-généré | Clé secrète Django |
| `DATABASE_URL` | Auto-configuré | URL base de données PostgreSQL |
| `ALLOWED_HOSTS` | `*.onrender.com,localhost,127.0.0.1` | Hosts autorisés |
| `CORS_ALLOWED_ORIGINS` | `https://*.onrender.com,http://localhost:3000` | CORS autorisé |
| `CSRF_TRUSTED_ORIGINS` | `https://*.onrender.com` | CSRF origins de confiance |
| `POPULATE_TEST_DATA` | `true` | Activer création données de test |

## Endpoints disponibles après déploiement

- **API Root** : `https://your-app.onrender.com/api/`
- **Documentation Swagger** : `https://your-app.onrender.com/api/docs/` ✅ CSRF-exempt
- **ReDoc** : `https://your-app.onrender.com/api/redoc/` ✅ CSRF-exempt  
- **Admin Django** : `https://your-app.onrender.com/admin/` ✅ Optimisé pour production
- **Authentification** : `https://your-app.onrender.com/api/auth/`

### 🔒 Sécurité CSRF

L'API est configurée pour fonctionner parfaitement en production avec :

- **Swagger UI** : Exemption CSRF automatique + middleware personnalisé
- **Admin Django** : Configuration CSRF optimisée avec `SameSite=Lax`
- **API Endpoints** : CSRF activé pour les vues sensibles
- **CORS** : Configuré pour les domaines de production

## Test de l'API

Une fois déployé, vous pouvez tester avec :

```bash
# Test de connexion
curl -X POST https://your-app.onrender.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "consumer@test.com", "password": "testpass123"}'

# Récupération des produits
curl https://your-app.onrender.com/api/products/products/
```

## Personnalisation

Pour désactiver la création des données de test en production :

1. Dans Render Dashboard, allez dans Environment
2. Changez `POPULATE_TEST_DATA` à `false`
3. Redéployez le service

## Monitoring

- Les logs sont visibles dans le Dashboard Render
- Healthcheck configuré sur `/api/` 
- Auto-restart en cas de crash

## Performance

Configuration optimisée pour Render Free Tier :
- 3 workers Gunicorn
- Timeout 120s
- Cache en mémoire (upgrade vers Redis si nécessaire)
- Static files via WhiteNoise
- Compression activée