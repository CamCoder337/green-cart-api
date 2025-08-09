# Configuration Render - Variables d'environnement

Puisque vous n'utilisez pas `render.yaml`, voici les variables d'environnement à configurer manuellement dans Render :

## Variables d'environnement requises :

```env
DJANGO_SETTINGS_MODULE=core.settings.production
DEBUG=false
SECRET_KEY=<auto-généré-par-render>
DATABASE_URL=<auto-fourni-par-render-postgres>
ALLOWED_HOSTS=*.onrender.com,localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=https://*.onrender.com,http://localhost:3000
CSRF_TRUSTED_ORIGINS=https://*.onrender.com
PORT=8000
WORKERS=3
POPULATE_TEST_DATA=true
```

## Étapes de configuration dans Render :

1. **Créer un Web Service**
   - Repository : votre repo GitHub
   - Branch : main
   - Runtime : Docker
   - Dockerfile : `./Dockerfile`

2. **Créer une base de données PostgreSQL**
   - Name : `greencart-db`
   - Puis copier l'URL de connexion dans `DATABASE_URL`

3. **Configurer les variables d'environnement**
   - Aller dans Environment 
   - Ajouter toutes les variables ci-dessus
   - Remplacer `*.onrender.com` par votre vraie URL une fois connue

4. **Deploy**
   - Le Dockerfile s'occupera de tout (migrations, données de test, etc.)

## URL finale esperée :
- API : `https://votre-app-name.onrender.com/api/`
- Swagger : `https://votre-app-name.onrender.com/api/docs/`
- Admin : `https://votre-app-name.onrender.com/admin/`

## Login par défaut après déploiement :
- **Admin** : admin / admin123
- **Test user** : consumer@test.com / testpass123