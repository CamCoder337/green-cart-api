# 🚀 Django Boilerplate

Une boilerplate Django moderne et complète avec les meilleures pratiques pour démarrer rapidement vos projets web.

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## 📋 Table des matières

- [Fonctionnalités](#-fonctionnalités)
- [Prérequis](#-prérequis)
- [Installation rapide](#-installation-rapide)
- [Structure du projet](#-structure-du-projet)
- [Configuration](#️-configuration)
- [Utilisation](#-utilisation)
- [Développement](#-développement)
- [Déploiement](#-déploiement)
- [Tests](#-tests)
- [Contribution](#-contribution)
- [License](#-license)

## ✨ Fonctionnalités

### 🏗️ Architecture
- **Django 5.0+** avec Python 3.13+
- **Settings modulaires** (development, production, testing)
- **Structure organisée** avec apps séparées
- **Variables d'environnement** pour la configuration

### 🔐 API & Authentification
- **Django REST Framework** configuré
- **Authentification par token**
- **CORS** configuré pour les frontends modernes
- **Pagination** et **filtrage** automatiques

### 🗄️ Base de données
- **SQLite** pour le développement
- **PostgreSQL** prêt pour la production
- **Migrations** automatisées

### ⚡ Performance & Cache
- **Redis** configuré pour le cache
- **WhiteNoise** pour les fichiers statiques
- **Celery** prêt pour les tâches asynchrones

### 🛠️ Outils de développement
- **Django Debug Toolbar** intégré
- **Pre-commit hooks** configurés
- **Tests** avec pytest
- **Code formatting** avec Black et isort

### 📦 Production Ready
- **Gunicorn** configuré
- **Logging** avancé
- **Monitoring** avec Sentry (optionnel)
- **Security settings** optimisés

## 🔧 Prérequis

- **Python 3.13+**
- **Git**
- **PostgreSQL** (optionnel, pour la production)
- **Redis** (optionnel, pour le cache)

## 🚀 Installation rapide

### 1. Cloner le projet

```bash
git clone https://github.com/votre-username/django-boilerplate.git mon-projet
cd mon-projet
```

### 2. Configurer l'environnement

```bash
# Créer l'environnement virtuel
python3.13 -m venv venv

# Activer l'environnement virtuel
# Sur Linux/Mac:
source venv/bin/activate
# Sur Windows:
# venv\Scripts\activate

# Installer les dépendances
pip install -r requirements-dev.txt
```

### 3. Configuration

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Générer une nouvelle clé secrète (optionnel)
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Copier la clé générée dans .env

# Créer la base de données
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser
```

### 4. Lancer le serveur

```bash
python manage.py runserver
```

🎉 **Votre projet est prêt !**
- **Interface** : http://127.0.0.1:8000/
- **API** : http://127.0.0.1:8000/api/
- **Admin** : http://127.0.0.1:8000/admin/

## 📁 Structure du projet

```
mon-projet/
├── 📁 core/                    # Configuration principale
│   ├── 📁 settings/           # Settings modulaires
│   │   ├── base.py           # Configuration de base
│   │   ├── development.py    # Développement
│   │   ├── production.py     # Production
│   │   └── testing.py        # Tests
│   ├── urls.py               # URLs principales
│   ├── wsgi.py               # Configuration WSGI
│   └── asgi.py               # Configuration ASGI
├── 📁 accounts/               # Gestion des utilisateurs
├── 📁 api/                    # API REST
├── 📁 static/                 # Fichiers statiques
├── 📁 media/                  # Fichiers média
├── 📁 templates/              # Templates HTML
├── 📁 logs/                   # Logs de l'application
├── 📄 requirements.txt        # Dépendances production
├── 📄 requirements-dev.txt    # Dépendances développement
├── 📄 .env.example           # Exemple de configuration
├── 📄 manage.py              # Script de gestion Django
└── 📄 README.md              # Cette documentation
```

## ⚙️ Configuration

### Variables d'environnement

Copiez `.env.example` vers `.env` et configurez selon vos besoins :

```env
# Configuration de base
SECRET_KEY=votre-clé-secrète-ici
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données
DATABASE_URL=sqlite:///db.sqlite3

# Email (optionnel)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app

# Cache Redis (optionnel)
REDIS_URL=redis://127.0.0.1:6379/1
```

### Environnements de configuration

```bash
# Développement (par défaut)
python manage.py runserver

# Production
DJANGO_SETTINGS_MODULE=core.settings.production python manage.py runserver

# Tests
DJANGO_SETTINGS_MODULE=core.settings.testing python manage.py test
```

## 📖 Utilisation

### Créer une nouvelle app

```bash
# Créer l'app
python manage.py startapp nom_app

# Ajouter dans core/settings/base.py
LOCAL_APPS = [
    'accounts',
    'api',
    'nom_app',  # ← Ajouter ici
]
```

### Travailler avec l'API

```python
# Dans votre app/serializers.py
from rest_framework import serializers

class MonSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonModel
        fields = '__all__'

# Dans votre app/views.py
from rest_framework import viewsets

class MonViewSet(viewsets.ModelViewSet):
    queryset = MonModel.objects.all()
    serializer_class = MonSerializer
```

### Base de données

```bash
# Créer des migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Réinitialiser la base de données
python manage.py flush
```

## 👨‍💻 Développement

### Outils de qualité de code

```bash
# Formatter le code
black .
isort .

# Vérifier la qualité
flake8

# Lancer tous les checks
pre-commit run --all-files
```

### Debug

Le **Django Debug Toolbar** est automatiquement activé en développement :
- Accédez à http://127.0.0.1:8000/__debug__/
- Consultez les panneaux de debug sur vos pages

### Shell Django amélioré

```bash
# Shell avec toutes les apps chargées
python manage.py shell_plus

# Avec affichage des requêtes SQL
python manage.py shell_plus --print-sql
```

## 🚀 Déploiement

### Avec Docker

```bash
# Construire l'image
docker build -t mon-projet .

# Lancer avec docker-compose
docker-compose up -d
```

### Production manuelle

```bash
# Variables d'environnement de production
export DJANGO_SETTINGS_MODULE=core.settings.production
export SECRET_KEY=votre-vraie-clé-secrète
export DATABASE_URL=postgresql://user:pass@localhost/dbname

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Lancer avec Gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Variables de production importantes

```env
DEBUG=False
SECRET_KEY=une-vraie-clé-secrète-complexe
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com
DATABASE_URL=postgresql://user:password@localhost:5432/production_db
REDIS_URL=redis://localhost:6379/0
EMAIL_HOST=smtp.votre-provider.com
SENTRY_DSN=https://votre-dsn@sentry.io/project-id
```

## 🧪 Tests

```bash
# Lancer tous les tests
python manage.py test

# Avec pytest (recommandé)
pytest

# Avec couverture de code
pytest --cov=.

# Tests spécifiques
pytest apps/accounts/tests/
```

### Écrire des tests

```python
# Dans votre app/tests.py
import pytest
from django.test import TestCase
from rest_framework.test import APITestCase

class MonModelTestCase(TestCase):
    def test_creation(self):
        # Votre test ici
        pass

@pytest.mark.django_db
class TestMonAPI(APITestCase):
    def test_api_endpoint(self):
        # Test d'API ici
        pass
```

## 📚 Ressources utiles

### Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python Decouple](https://github.com/henriquebastos/python-decouple)

### Commandes utiles

```bash
# Informations sur le projet
python manage.py check
python manage.py showmigrations
python manage.py dbshell

# Gestion des utilisateurs
python manage.py changepassword username
python manage.py createsuperuser

# Cache
python manage.py clear_cache
```

## 🤝 Contribution

1. **Fork** le projet
2. **Créez** votre branche (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements (`git commit -m 'Add: Amazing Feature'`)
4. **Push** vers la branche (`git push origin feature/AmazingFeature`)
5. **Ouvrez** une Pull Request

### Standards de code

- Utilisez **Black** pour le formatage
- Suivez **PEP 8**
- Ajoutez des **tests** pour les nouvelles fonctionnalités
- Documentez votre code

## 🐛 Problèmes courants

### Erreur de base de données
```bash
# Réinitialiser les migrations
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete
python manage.py makemigrations
python manage.py migrate
```

### Erreur de clé secrète
```bash
# Générer une nouvelle clé
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Debug Toolbar ne s'affiche pas
```bash
# Vérifier INTERNAL_IPS dans settings/development.py
# Vérifier que DEBUG=True
# Redémarrer le serveur
```

## 📄 License

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 👨‍💻 Auteur

**Camcoder337** - [@camcoder337](https://github.com/camcoder337)

---

⭐ **N'hésitez pas à donner une étoile si ce projet vous a aidé !**

## 🔗 Liens utiles

- [Signaler un bug](https://github.com/votre-username/django-boilerplate/issues)
- [Demander une fonctionnalité](https://github.com/votre-username/django-boilerplate/issues)
- [Documentation complète](https://github.com/votre-username/django-boilerplate/wiki)

---

*Made with ❤️ and Django*