"""
Settings pour l'environnement de production.
"""
import logging

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
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# ==============================================================================
# DATABASE CONFIGURATION
# ==============================================================================

DATABASES = {
    'default': config('DATABASE_URL', cast=db_url)
}

# Configuration avancée pour PostgreSQL en production
DATABASES['default'].update({
    'CONN_MAX_AGE': config('DB_CONN_MAX_AGE', default=60, cast=int),
    'OPTIONS': {
        'connect_timeout': 10,
        'options': '-c default_transaction_isolation=serializable'
    }
})

# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

# SSL/TLS Configuration
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

# Session Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_COOKIE_SAMESITE = 'Lax'  # Allow admin/swagger to work

# CSRF Security
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Lax'  # Allow cross-origin admin access
CSRF_USE_SESSIONS = True  # Use sessions for CSRF token storage

# ==============================================================================
# CACHE CONFIGURATION
# ==============================================================================

# Fallback to local memory cache if Redis not available
REDIS_URL = config('REDIS_URL', default=None)
if REDIS_URL:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': REDIS_URL,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            },
            'KEY_PREFIX': config('CACHE_KEY_PREFIX', default='greencart'),
            'TIMEOUT': config('CACHE_TIMEOUT', default=300, cast=int),
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'greencart-cache',
        }
    }

# ==============================================================================
# EMAIL CONFIGURATION
# ==============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# ==============================================================================
# LOGGING CONFIGURATION
# ==============================================================================

# Créer le dossier logs s'il n'existe pas
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'json': {
            'format': '{"level": "{levelname}", "time": "{asctime}", "module": "{module}", "message": "{message}"}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOGS_DIR / 'django_error.log',
            'maxBytes': 1024 * 1024 * 10,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'level': 'ERROR',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'error_file'],
            'level': 'WARNING',
            'propagate': False,
        },
    },
}

# ==============================================================================
# PERFORMANCE SETTINGS
# ==============================================================================

# Compression et optimisation des fichiers statiques
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ==============================================================================
# CORS CONFIGURATION
# ==============================================================================

CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

CORS_ALLOW_CREDENTIALS = True

# ==============================================================================
# CSRF CONFIGURATION
# ==============================================================================

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='',
    cast=lambda v: [s.strip() for s in v.split(',') if s.strip()]
)

# ==============================================================================
# CELERY CONFIGURATION (pour les tâches asynchrones)
# ==============================================================================

# Only configure Celery if Redis is available
if REDIS_URL:
    CELERY_BROKER_URL = config('CELERY_BROKER_URL', default=REDIS_URL)
    CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default=REDIS_URL)
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
    CELERY_TIMEZONE = TIME_ZONE

# ==============================================================================
# MONITORING & SENTRY (optionnel)
# ==============================================================================

SENTRY_DSN = config('SENTRY_DSN', default=None)
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    from sentry_sdk.integrations.logging import LoggingIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(auto_enabling=True),
            LoggingIntegration(level=logging.INFO, event_level=logging.ERROR),
        ],
        traces_sample_rate=0.1,
        send_default_pii=True,
        environment=config('ENVIRONMENT', default='production'),
    )

# ==============================================================================
# SWAGGER CONFIGURATION FOR PRODUCTION
# ==============================================================================

# Override Swagger servers for production
SPECTACULAR_SETTINGS = SPECTACULAR_SETTINGS.copy()  # Copy from base settings
SPECTACULAR_SETTINGS.update({
    'SERVERS': [
        {'url': 'https://' + ALLOWED_HOSTS[0] + '/api', 'description': 'Production server'} if ALLOWED_HOSTS and not ALLOWED_HOSTS[0].startswith('*') else {'url': '/api', 'description': 'Current server'},
        {'url': 'http://127.0.0.1:8000/api', 'description': 'Local development'},
    ],
    'SWAGGER_UI_SETTINGS': SPECTACULAR_SETTINGS['SWAGGER_UI_SETTINGS'].copy(),
})

# Enhance Swagger for production
SPECTACULAR_SETTINGS['SWAGGER_UI_SETTINGS'].update({
    'defaultModelsExpandDepth': 2,
    'defaultModelExpandDepth': 2,
    'displayRequestDuration': True,
    'requestInterceptor': '''(request) => {
        // Add CSRF token for session auth if available
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;
        if (csrfToken && request.headers) {
            request.headers['X-CSRFToken'] = csrfToken;
        }
        return request;
    }''',
})