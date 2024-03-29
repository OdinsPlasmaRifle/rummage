import os

from celery.schedules import crontab
from .secrets import *


DEBUG = os.environ.get('DEBUG', False)

SECRET_KEY = os.environ.get('DJANGO_SECRET', '')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'rummage.urls'

WSGI_APPLICATION = 'rummage.wsgi.application'

VERSION = '1.0.0'

SITE_ID = 1

# Installed apps
# ------------------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'rummage',
]

# Middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# AutoField
# ------------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# CORS headers
# ------------------------------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# Template files
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/howto/static-files/
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'rummage/templates/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
# ------------------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'postgres'),
        'USER': os.environ.get('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.environ.get('POSTGRES_HOST', 'postgres'),
        'PORT': os.environ.get('POSTGRES_PORT', 5432),
        'OPTIONS': {
            'connect_timeout': 25,
        }
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/
# ------------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# ------------------------------------------------------------------------------
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'var/www/static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'var/www/media')

# REST FRAMEWORK ~ http://www.django-rest-framework.org/
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '60/minute'
    },
    'DEFAULT_VERSION': '1',
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15
}

# Spectacular
# ------------------------------------------------------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'Rummage API',
    'DESCRIPTION': 'Rummage API',
    'VERSION': '1',

    # List of servers.
    'SERVERS': [
        {"url": os.environ.get(
            'BASE_URL', "https://rummage.odinsplasmarifle.com"
        )}
    ],

    # Swagger UI
    'SWAGGER_UI_DIST': 'SIDECAR',
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'SWAGGER_UI_SETTINGS': {
        'docExpansion': 'none',
        'showExtensions': False,
        'defaultModelRendering': "example",
        'displayOperationId': True
    },

    # Redoc
    'REDOC_DIST': 'SIDECAR',
    'REDOC_UI_SETTINGS': {
        'lazyRendering': True,
        'nativeScrollbars': True,
        'requiredPropsFirst': True,
        'showExtensions': True
    },
}

# Celery
# ------------------------------------------------------------------------------
if os.environ.get('SKIP_TASK_QUEUE') in ['True', 'true', True]:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True

CELERY_TASK_SERIALIZER = 'msgpack'
CELERY_ACCEPT_CONTENT = ['msgpack']

project_id = os.environ.get('CELERY_ID', 'local')
CELERY_TASK_DEFAULT_QUEUE = '-'.join(('general', project_id))

RABBITMQ_HOST = os.environ.get('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = os.environ.get('RABBITMQ_PORT', '5672')

CELERY_BROKER_URL = 'amqp://{user}:{password}@{hostname}/{vhost}'.format(
    user=os.environ.get('RABBITMQ_USER', 'guest'),
    password=os.environ.get('RABBITMQ_PASSWORD', 'guest'),
    hostname="%s:%s" % (RABBITMQ_HOST, RABBITMQ_PORT),
    vhost=os.environ.get('RABBITMQ_ENV_RABBITMQ_DEFAULT_VHOST', '/')
)

CELERY_IGNORE_RESULT = True

CELERY_BEAT_SCHEDULE = {
    'clear_searches': {
        'task': 'rummage.tasks.clear_searches',
        'schedule': crontab(hour=1),
        'args': ()
    }
}

# Logging
# ------------------------------------------------------------------------------
from django.utils.log import DEFAULT_LOGGING

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s "
                      "%(process)d %(thread)d %(message)s"
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    "loggers": {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
}
