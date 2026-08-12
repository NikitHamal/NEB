"""
Django settings for NEBians backend.
Production defaults are intentionally strict. Use .env.example as the only
committed template; never deploy with DEBUG=True or fallback secrets.
"""
import os
import re
import sys
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env', override=True)


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return str(value).strip().lower() in {'1', 'true', 'yes', 'on'}


def env_list(name, default=''):
    value = os.environ.get(name, default)
    return [item.strip() for item in value.split(',') if item.strip()]


# Domains that should be accepted in ALLOWED_HOSTS but not exact-match.
# Use this for things like '.trycloudflare.com' which is a wildcard
# matching any trycloudflare subdomain.
_env_extra_hosts = os.environ.get('ALLOWED_HOSTS_GLOB', '')
ALLOWED_HOSTS_GLOB = [item.strip() for item in _env_extra_hosts.split(',') if item.strip()]


# Suffixes that should match any subdomain (e.g. '.trycloudflare.com' matches
# 'fresh-xyz.trycloudflare.com'). Populated from ALLOWED_HOSTS_GLOB env var.
ALLOWED_HOST_SUFFIXES = [h.lstrip('.') for h in ALLOWED_HOSTS_GLOB if h.startswith('.')]


DEBUG = env_bool('DEBUG', False)
SECRET_KEY = os.environ.get('SECRET_KEY', '')
if not SECRET_KEY or SECRET_KEY == 'django-insecure-change-me-in-production':
    if DEBUG:
        SECRET_KEY = 'django-insecure-local-development-only-change-me'
    else:
        raise ImproperlyConfigured('SECRET_KEY must be set to a strong unique value when DEBUG=False')

ADMIN_API_SALT = os.environ.get('ADMIN_API_SALT', '')
if not ADMIN_API_SALT:
    if DEBUG:
        ADMIN_API_SALT = SECRET_KEY
    else:
        raise ImproperlyConfigured('ADMIN_API_SALT must be set when DEBUG=False')

# Shared secret for the Consica app AI bridge endpoint.
# Must be set in .env for both dev and production.
CONSICA_BRIDGE_KEY = os.environ.get('CONSICA_BRIDGE_KEY', '')
if not CONSICA_BRIDGE_KEY:
    if DEBUG:
        CONSICA_BRIDGE_KEY = 'dev-consica-bridge-key-change-in-prod'
    else:
        raise ImproperlyConfigured('CONSICA_BRIDGE_KEY must be set when DEBUG=False')

ALLOWED_HOSTS = env_list(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,nebians.consica.com.np,www.nebians.consica.com.np',
)

# Wildcard patterns (e.g. '.trycloudflare.com' matches any subdomain).
# Combined with ALLOWED_HOSTS for the request host check in middleware.
ALLOWED_HOSTS = list(ALLOWED_HOSTS) + list(ALLOWED_HOSTS_GLOB)

INSTALLED_APPS = [
    'daphne',
    'django_htmx',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
    'rest_framework',
    'corsheaders',
    'api',
    'web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'nebians.middleware.AllowedHostMiddleware',
    'nebians.middleware.BearerCsrfExemptMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_htmx.middleware.HtmxMiddleware',
    'nebians.middleware.SecurityHeadersMiddleware',
    'nebians.middleware.PageViewTrackingMiddleware',
]

ROOT_URLCONF = 'nebians.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'nebians.middleware.csp_nonce_context',
            ],
        },
    },
]

LOGIN_URL = '/admin/'
WSGI_APPLICATION = 'nebians.wsgi.application'
ASGI_APPLICATION = 'nebians.asgi.application'

# Channels layer: Redis-backed so broadcasts fan out across daphne + any
# Passenger workers. Falls back to in-memory if Redis isn't configured
# (single-process dev only).
if os.environ.get('CACHE_BACKEND') == 'django.core.cache.backends.redis.RedisCache':
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [os.environ.get('CACHE_LOCATION', 'redis://127.0.0.1:6379/0')],
                'capacity': 1500,
                'expiry': 30,
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {'BACKEND': 'channels.layers.InMemoryChannelLayer'},
    }

# Database - MySQL in production, SQLite only when explicitly requested.
if os.environ.get('DB_ENGINE') == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.environ.get('DB_NAME', 'nebians_db'),
            'USER': os.environ.get('DB_USER', 'nebians_user'),
            'PASSWORD': os.environ.get('DB_PASSWORD', ''),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '3306'),
            'OPTIONS': {'charset': 'utf8mb4', 'init_command': "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"},
            'CONN_MAX_AGE': int(os.environ.get('DB_CONN_MAX_AGE', '60')),
            'CONN_HEALTH_CHECKS': os.environ.get('DB_CONN_HEALTH_CHECKS', 'True') == 'True',
        }
    }

ADMINS = [('NEBians Admin', os.environ.get('ADMIN_EMAIL', 'noreply@nebians.consica.com.np'))]
SERVER_EMAIL = os.environ.get('SERVER_EMAIL', 'noreply@nebians.consica.com.np')

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

def _immutable_file_test(path, _url=None):
    p = path.replace('\\', '/')
    return 'web/js/needle2/' in p or (_url is not None and 'web/js/needle2/' in _url)

WHITENOISE_IMMUTABLE_FILE_TEST = _immutable_file_test

MEDIA_URL = '/media/'
MEDIA_ROOT = (BASE_DIR / 'public' / 'media') if (BASE_DIR / 'public').exists() else (BASE_DIR / 'media')
PROFILE_PHOTO_MAX_BYTES = int(os.environ.get('PROFILE_PHOTO_MAX_BYTES', str(5 * 1024 * 1024)))
FILE_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get('FILE_UPLOAD_MAX_MEMORY_SIZE', str(110 * 1024 * 1024)))
DATA_UPLOAD_MAX_MEMORY_SIZE = int(os.environ.get('DATA_UPLOAD_MAX_MEMORY_SIZE', str(110 * 1024 * 1024)))

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    'default': {
        'BACKEND': os.environ.get('CACHE_BACKEND', 'django.core.cache.backends.locmem.LocMemCache'),
        'LOCATION': os.environ.get('CACHE_LOCATION', 'nebians-default-cache'),
    },
}

# Redis cache configuration (set CACHE_BACKEND=django.core.cache.backends.redis.RedisCache
# and CACHE_LOCATION=redis://localhost:6379/0 in .env to enable)
if os.environ.get('CACHE_BACKEND') == 'django.core.cache.backends.redis.RedisCache':
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': os.environ.get('CACHE_LOCATION', 'redis://127.0.0.1:6379/0'),
    }

# Session backend — cached_db writes to both DB and cache, so existing sessions
# survive cache clears and Redis restarts. Falls back to DB-only when no Redis.
SESSION_ENGINE = os.environ.get(
    'SESSION_ENGINE',
    'django.contrib.sessions.backends.cached_db' if os.environ.get('CACHE_BACKEND') == 'django.core.cache.backends.redis.RedisCache'
    else 'django.contrib.sessions.backends.db'
)
SESSION_CACHE_ALIAS = 'default'

MEILISEARCH_URL = os.environ.get('MEILISEARCH_URL', '')
MEILISEARCH_API_KEY = os.environ.get('MEILISEARCH_API_KEY', '')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'api.authentication.AuthTokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': os.environ.get('DRF_ANON_THROTTLE', '100/hour'),
        'user': os.environ.get('DRF_USER_THROTTLE', '1000/hour'),
        'auth': os.environ.get('DRF_AUTH_THROTTLE', '60/minute'),
        'verification': os.environ.get('DRF_VERIFICATION_THROTTLE', '6/hour'),
        'write_action': os.environ.get('DRF_WRITE_ACTION_THROTTLE', '30/minute'),
        'report': os.environ.get('DRF_REPORT_THROTTLE', '10/hour'),
        'search': os.environ.get('DRF_SEARCH_THROTTLE', '60/minute'),
        'upload': os.environ.get('DRF_UPLOAD_THROTTLE', '10/hour'),
        'view_increment': os.environ.get('DRF_VIEW_INCREMENT_THROTTLE', '60/minute'),
        'arena_chat': os.environ.get('DRF_ARENA_CHAT_THROTTLE', '60/minute'),
        'arena_list': os.environ.get('DRF_ARENA_LIST_THROTTLE', '120/minute'),
        'signup': os.environ.get('DRF_SIGNUP_THROTTLE', '5/hour'),
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(os.environ.get('API_PAGE_SIZE', '50')),
}

CORS_ALLOWED_ORIGINS = env_list(
    'CORS_ALLOWED_ORIGINS',
    'https://nebians.consica.com.np,http://localhost:8000,http://127.0.0.1:8000',
)
CSRF_TRUSTED_ORIGINS = env_list(
    'CSRF_TRUSTED_ORIGINS',
    'https://nebians.consica.com.np,https://www.nebians.consica.com.np',
)

# HTTPS, cookies, browser hardening.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env_bool('SECURE_SSL_REDIRECT', False)
SESSION_COOKIE_SECURE = env_bool('SESSION_COOKIE_SECURE', False)
CSRF_COOKIE_SECURE = env_bool('CSRF_COOKIE_SECURE', False)
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SECURE_HSTS_SECONDS = int(os.environ.get('SECURE_HSTS_SECONDS', '31536000' if not DEBUG else '0'))
SECURE_HSTS_INCLUDE_SUBDOMAINS = env_bool('SECURE_HSTS_INCLUDE_SUBDOMAINS', not DEBUG)
SECURE_HSTS_PRELOAD = env_bool('SECURE_HSTS_PRELOAD', not DEBUG)
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
X_FRAME_OPTIONS = 'DENY'

# Google OAuth / Firebase config.
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID', '')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET', '')

# GitHub OAuth.
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID', '')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET', '')
BACKGROUND_AGENT_PUBLIC_URL = os.environ.get('BACKGROUND_AGENT_PUBLIC_URL', '').rstrip('/')

# Server-wide fallback keys for official LLM providers (lowest priority —
# user BYOK rows and admin bot configs override these). Drop a free key from
# the Agnes console here to give every NEBian Agnes out of the box.
LLM_PROVIDER_KEYS = {
    'agnes': os.environ.get('AGNES_API_KEY', ''),
    'openai': os.environ.get('OPENAI_API_KEY', ''),
    'anthropic': os.environ.get('ANTHROPIC_API_KEY', ''),
    'gemini': os.environ.get('GEMINI_API_KEY', ''),
    'deepseek': os.environ.get('DEEPSEEK_API_KEY', ''),
    'agentrouter': os.environ.get('AGENTROUTER_API_KEY', ''),
}

# LLM call time budget for background-agent official providers (seconds).
BACKGROUND_AGENT_PROVIDER_TIMEOUT = int(os.environ.get('BACKGROUND_AGENT_PROVIDER_TIMEOUT', '300'))
# Context window for agent sessions (default 1M — Qwen models all support 1M).
BACKGROUND_AGENT_CONTEXT_WINDOW_TOKENS = int(os.environ.get('BACKGROUND_AGENT_CONTEXT_WINDOW_TOKENS', '1000000'))
BACKGROUND_AGENT_ALLOW_LOCAL_EXECUTION = os.environ.get('BACKGROUND_AGENT_ALLOW_LOCAL_EXECUTION', 'True').lower() in ('1', 'true', 'yes')
FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY', '')
FIREBASE_AUTH_DOMAIN = os.environ.get('FIREBASE_AUTH_DOMAIN', '')
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', '')
FIREBASE_STORAGE_BUCKET = os.environ.get('FIREBASE_STORAGE_BUCKET', '')
FIREBASE_SENDER_ID = os.environ.get('FIREBASE_SENDER_ID', '')
FIREBASE_APP_ID = os.environ.get('FIREBASE_APP_ID', '')

# Email configuration.
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'nebians.consica.com.np')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', '465'))
EMAIL_USE_TLS = env_bool('EMAIL_USE_TLS', False)
EMAIL_USE_SSL = env_bool('EMAIL_USE_SSL', not EMAIL_USE_TLS)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'noreply@nebians.consica.com.np')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'NEBians <noreply@nebians.consica.com.np>')

WEB_API_BASE_URL = os.environ.get('WEB_API_BASE_URL', 'http://127.0.0.1:8000/api')

LOG_DIR = Path(os.environ.get('LOG_DIR', BASE_DIR / 'logs'))
LOG_DIR.mkdir(exist_ok=True)

class SensitiveDataFilter(logging.Filter):
    REDACT_KEYS = ('token', 'auth', 'password', 'secret', 'credential', 'code')
    _PATTERN = re.compile(
        r'(' + '|'.join(REDACT_KEYS) + r')\s*[=:]\s*[^\s,;]+',
        re.IGNORECASE,
    )

    def filter(self, record):
        message = record.getMessage()
        message = self._PATTERN.sub(r'\1[REDACTED]', message)
        record.msg = message
        record.args = ()
        return True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'redact_sensitive': {'()': 'nebians.settings.SensitiveDataFilter'},
    },
    'formatters': {
        'verbose': {'format': '[{asctime}] {levelname} {name} {message}', 'style': '{'},
        'simple': {'format': '{levelname} {message}', 'style': '{'},
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'verbose',
            'filters': ['redact_sensitive'],
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'nebians.log',
            'maxBytes': int(os.environ.get('LOG_MAX_BYTES', '10485760')),
            'backupCount': int(os.environ.get('LOG_BACKUP_COUNT', '5')),
            'formatter': 'verbose',
            'filters': ['redact_sensitive'],
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': False,
        },
    },
    'loggers': {
        'api': {'handlers': ['console', 'file'], 'level': os.environ.get('LOG_LEVEL', 'INFO'), 'propagate': False},
        'web': {'handlers': ['console', 'file'], 'level': os.environ.get('LOG_LEVEL', 'INFO'), 'propagate': False},
        'django.request': {'handlers': ['console', 'file', 'mail_admins'], 'level': 'ERROR', 'propagate': False},
    },
    'root': {'handlers': ['console', 'file'], 'level': os.environ.get('LOG_LEVEL', 'INFO')},
}
