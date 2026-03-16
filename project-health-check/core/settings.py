from pathlib import Path
import logging
import os
import environ
from datetime import timedelta


logger = logging.getLogger(__name__)

# ==============================================================================
# ENV
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
LOG_LEVEL = env("LOG_LEVEL", default="INFO")

# ==============================================================================
# DJANGO-BASE
# ==============================================================================

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# ==============================================================================
# APPLICATIONS
# ==============================================================================

PACKAGES = [
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
]

DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "userauth",
    "services",
    "healthcheck",
]

INSTALLED_APPS = PACKAGES + DJANGO_APPS + PROJECT_APPS

AUTH_USER_MODEL = "userauth.User"

# ==============================================================================
# MIDDLEWARE
# ==============================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==============================================================================
# URLS AND TEMPLATES
# ==============================================================================

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# ==============================================================================
# DATABASE
# ==============================================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DATABASE_NAME", default="trades4u"),
        "USER": env("DATABASE_USER", default="root"),
        "PASSWORD": env("DATABASE_PASSWORD", default="root"),
        "HOST": env("DATABASE_HOST", default="localhost"),
    }
}

# ==============================================================================
# CELERY
# ==============================================================================

CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND", default="redis://127.0.0.1:6379/0")
CELERY_ACCEPT_CONTENT = env.list("CELERY_ACCEPT_CONTENT", default=["json"])
CELERY_TASK_SERIALIZER = env("CELERY_TASK_SERIALIZER", default="json")
CELERY_RESULT_SERIALIZER = env("CELERY_RESULT_SERIALIZER", default="json")
CELERY_TIMEZONE = env("CELERY_TIMEZONE", default="UTC")
CELERY_TASK_TRACK_STARTED = env("CELERY_TASK_TRACK_STARTED", default=True)
CELERY_TASK_TIME_LIMIT = env.int("CELERY_TASK_TIME_LIMIT", default=1800)

CELERY_REDIS_MAX_CONNECTIONS = env.int("CELERY_REDIS_MAX_CONNECTIONS", default=20)
CELERY_BROKER_CONNECTION_RETRY = env("CELERY_BROKER_CONNECTION_RETRY", default=True)
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = env(
    "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP", default=True
)
CELERY_BROKER_CONNECTION_MAX_RETRIES = env(
    "CELERY_BROKER_CONNECTION_MAX_RETRIES", default=True
)
CELERY_BROKER_POOL_LIMIT = env("CELERY_BROKER_POOL_LIMIT", default=None)
ACCESS_TOKEN_CACHE_TTL = env("ACCESS_TOKEN_CACHE_TTL", default=172800)

# ==============================================================================
# CACHES
# ==============================================================================

CACHES = {
    "default": {
        "BACKEND": env("CACHES_ENGINE", default="django_redis.cache.RedisCache"),
        "LOCATION": env("REDIS_CLIENTS", default="redis://localhost:6379/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# ==============================================================================
# AUTHENTICATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "rest_framework.permissions.DjangoModelPermissions",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "services.renderer.CustomJSONRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
}


# ==============================================================================
# JWT
# ==============================================================================

ACCESS_TOKEN_LIFETIME = env.int("ACCESS_TOKEN_LIFETIME", default=1800)
REFRESH_TOKEN_LIFETIME = env.int("REFRESH_TOKEN_LIFETIME", default=1)

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=ACCESS_TOKEN_LIFETIME),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=REFRESH_TOKEN_LIFETIME),
    "AUTH_HEADER_TYPES": ("Bearer"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "CHECK_REVOKE_TOKEN": True,
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "USER_AUTHENTICATION_RULE": "accounts.models.User.is_active",
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "USER_ID_FIELD": "id",
}

# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True


# ==============================================================================
# LOGGING
# ==============================================================================

LOG_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s"},
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(module)s:%(lineno)d %(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "level": LOG_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": LOG_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "project_health_check.log"),
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
        },
        "django.request": {
            "handlers": ["file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
}


# ==============================================================================
# STATIC & MEDIA
# ==============================================================================

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ==============================================================================
# EMAIL
# ==============================================================================

EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = env("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = env("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="test@gmail.com")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="Test@123")

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
