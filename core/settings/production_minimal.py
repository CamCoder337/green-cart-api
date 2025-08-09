"""
Settings pour l'environnement de production - VERSION MINIMALISTE.
"""
from .base import *
from decouple import config

# ==============================================================================
# DEBUG CONFIGURATION
# ==============================================================================
DEBUG = False

# ==============================================================================
# HOST CONFIGURATION
# ==============================================================================
ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='*.onrender.com,gc-api-3yjt.onrender.com,localhost,127.0.0.1',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================
DATABASES = {
    'default': config(
        'DATABASE_URL', 
        default='sqlite:///db.sqlite3',
        cast=db_url
    )
}

# ==============================================================================
# SECURITY SETTINGS - MINIMAL
# ==============================================================================
SECURE_SSL_REDIRECT = False  # Render handles this
SESSION_COOKIE_SECURE = False  # Render handles this
CSRF_COOKIE_SECURE = False  # Render handles this

# ==============================================================================
# CORS CONFIGURATION
# ==============================================================================
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='https://*.onrender.com,http://localhost:3000',
    cast=lambda v: [s.strip() for s in v.split(',')]
)
CORS_ALLOW_CREDENTIALS = True

# ==============================================================================
# DISABLE LOGGING TO AVOID ERRORS
# ==============================================================================
LOGGING_CONFIG = None

# ==============================================================================
# CSRF CONFIGURATION - DISABLE FOR API ONLY DEPLOYMENT
# ==============================================================================
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SECURE = False
USE_TZ = True

# ==============================================================================
# STATIC FILES
# ==============================================================================
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'