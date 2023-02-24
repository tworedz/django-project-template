import os

from environ import Env
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.huey import HueyIntegration
from sentry_sdk.integrations.redis import RedisIntegration


env = Env()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

Env.read_env(os.path.join(os.path.dirname(BASE_DIR), ".env"))

SECRET_KEY = env.str("SECRET_KEY", default="debug")

DEBUG = env.bool("APP_DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default="*")

INSTALLED_APPS = [
    "jet.dashboard",
    "jet",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # third party apps
    "rest_framework",
    "rest_framework.authtoken",
    "fcm_django",
    "drf_spectacular",
    "silk",
    "solo",
    "huey.contrib.djhuey",
    # project apps
    "firebase_auth",
    "users",
    "contacts",
    "news",
    "meals",
    "orders",
    "notifications",
    "bonus_logging",
    "telegram",
    "integration",
]

MIDDLEWARE = [
    "silk.middleware.SilkyMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": env.str("DB_ENGINE", default="django.db.backends.postgresql"),
        "NAME": env.str("POSTGRES_DB", default="{{ project_name }}"),
        "USER": env.str("POSTGRES_USER", default="postgres"),
        "PASSWORD": env.str("POSTGRES_PASSWORD", default="postgres"),
        "HOST": env.str("POSTGRES_HOST", default="localhost"),
        "PORT": env.int("POSTGRES_PORT", default=5432),
    },
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
X_FRAME_OPTIONS = "SAMEORIGIN"

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "ru"

TIME_ZONE = env.str("TIME_ZONE", "Asia/Bishkek")

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles/")

AUTH_USER_MODEL = "users.User"

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "core.pagination.Pagination",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "core.exceptions.drf_exception_handler",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "{{ project_title }} documentation",
    "VERSION": "0.0.1",
    "SCHEMA_PATH_PREFIX": "/api/v[0-9]",
    "SCHEMA_PATH_PREFIX_TRIM": False,
    "COMPONENT_SPLIT_REQUEST": True,  # convert "string image" to "binary image"
    "SERVE_INCLUDE_SCHEMA": False,
    "SERVE_AUTHENTICATION": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "SWAGGER_UI_SETTINGS": {
        "defaultModelExpandDepth": 3,
        "defaultModelRendering": "model",
        "filter": True,
        "showCommonExtensions": True,
        "persistAuthorization": True,
        "displayOperationId": True,
        "deepLinking": True,
        "docExpansion": "none",
    },
    "TAGS": [
        {
            "name": "users",
            "externalDocs": {
                "description": "Firebase token explanation",
                "url": "https://firebase.google.com/docs/auth/admin/verify-id-tokens",
            },
        },
    ],
}

# Silk
SILKY_AUTHENTICATION = True  # User must login
SILKY_AUTHORISATION = True  # User must have permissions
SILKY_META = True
SILKY_INTERCEPT_PERCENT = env.int("SILKY_INTERCEPT_PERCENT", default=100)
SILKY_MAX_RECORDED_REQUESTS = 10**4
SILKY_ANALYZE_QUERIES = True
SILKY_JSON_ENSURE_ASCII = False

# Jet settings
JET_SIDE_MENU_COMPACT = True

# Firebase settings
FCM_DJANGO_SETTINGS = {
    "ONE_DEVICE_PER_USER": False,
    "APP_VERBOSE_NAME": "FCM Django",
    "DELETE_INACTIVE_DEVICES": True,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}

GOOGLE_APPLICATION_CREDENTIALS = env.str(
    "GOOGLE_APPLICATION_CREDENTIALS",
    os.path.join(BASE_DIR, "firebase-sdk.json"),
)

# Redis
REDIS_HOST = env.str("REDIS_HOST", default="localhost")
REDIS_PORT = env.int("REDIS_PORT", default=6379)
REDIS_DB = env.int("REDIS_DB", default=0)

# Huey
HUEY = {
    "huey_class": "huey.RedisHuey",
    "name": env.str("POSTGRES_DB", default="{{ project_name }}"),
    "results": True,
    "immediate": env.bool("HUEY_IMMEDIATE", default=False),
    "connection": {
        "host": REDIS_HOST,
        "port": REDIS_PORT,
        "db": REDIS_DB,
        "connection_pool": None,
        "read_timeout": 1,
        "url": None,
    },
    "consumer": {
        "workers": 1,
        "worker_type": "thread",
        "initial_delay": 0.1,
        "backoff": 1.15,
        "max_delay": 10.0,
        "scheduler_interval": 1,
        "periodic": True,
        "check_worker_health": True,
        "health_check_interval": 1,
    },
}

# Sentry
sentry_sdk.init(
    dsn=env.str("SENTRY_DSN", default=""),
    integrations=[
        DjangoIntegration(),
        RedisIntegration(),
        HueyIntegration(),
    ],
    traces_sample_rate=1.0,
    send_default_pii=True,
)
# TODO: configure logging
